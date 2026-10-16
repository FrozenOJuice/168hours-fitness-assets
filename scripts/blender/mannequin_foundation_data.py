"""Graphical-data adapter for pinned CC0 MakeHuman topology; original Python implementation."""
from pathlib import Path
import json,math
import numpy as np
from mathutils import Vector,Matrix
from build_anatomical_mannequin import R,A,ID,RID,SOURCE,SK,CAT
REF=A/'references/makehuman'
def read_mesh():
 vertices=[];faces=[];group=''
 for line in (REF/'base.obj').read_text().splitlines():
  if line.startswith('v '):vertices.append([float(x) for x in line.split()[1:]])
  elif line.startswith('g '):group=line[2:]
  elif line.startswith('f ') and group=='body':faces.append([int(s.split('/')[0])-1 for s in line.split()[1:]])
 ids=sorted({v for f in faces for v in f});remap={old:i for i,old in enumerate(ids)};allxyz=np.array(vertices)[:,[0,2,1]];body=allxyz[ids];floor=body[:,2].min();scale=1.75/(body[:,2].max()-floor);allxyz[:,2]-=floor;allxyz*=scale
 return allxyz,ids,[[remap[v] for v in f] for f in faces]
def source_joints(xyz):
 data=json.loads((REF/'default.mhskel').read_text());j={n:Vector(np.mean(xyz[ids],axis=0)) for n,ids in data['joints'].items()}
 return {n:(j[b['head']],j[b['tail']]) for n,b in data['bones'].items()}
def frame(a,b,z=(0,1,0)):
 y=(Vector(b)-Vector(a)).normalized();z=Vector(z);z-=y*z.dot(y)
 if z.length<1e-6:z=Vector((0,0,1))-y*y.z
 z.normalize();x=y.cross(z).normalized();m=Matrix((x,y,z)).transposed().to_4x4();m.translation=a;return m

def weight_map(name):
 side='l' if name.endswith('.L') else 'r';stem=name.split('.')[0]
 if stem.startswith('finger'):
  d,i=stem[6:].split('-');return ['thumb','index','middle','ring','little'][int(d)-1]+f'_{int(i):02}_'+side
 if stem in ['upperarm01','upperarm02']:return 'upper_arm_'+side
 if stem in ['lowerarm01','lowerarm02']:return 'forearm_'+side
 if stem=='wrist' or stem.startswith('metacarpal'):return 'hand_'+side
 if stem in ['clavicle','shoulder01']:return 'clavicle_'+side
 if stem in ['upperleg01','upperleg02']:return 'thigh_'+side
 if stem in ['lowerleg01','lowerleg02']:return 'shin_'+side
 if stem=='foot':return 'foot_'+side
 if stem.startswith('toe'):return 'toe_'+side
 if stem=='root' or stem=='pelvis' or stem in ['spine05','spine04']:return 'pelvis'
 if stem=='spine03':return 'spine_01'
 if stem in ['spine02','breast']:return 'spine_02'
 if stem=='spine01':return 'spine_03'
 if stem.startswith('neck'):return 'neck'
 return 'head'

def canonical_data():
 xyz,ids,faces=read_mesh();src=source_joints(xyz);normals={};g={'root':(Vector((0,0,0)),Vector((0,0,.1)))};s={}
 axial=[('pelvis',src['root'][1],src['spine04'][1]),('spine_01',src['spine04'][1],src['spine03'][1]),('spine_02',src['spine03'][1],src['spine02'][1]),('spine_03',src['spine02'][1],src['spine01'][1]),('neck',src['spine01'][1],src['head'][0]),('head',src['head'][0],src['head'][1])]
 for name,a,b in axial:s[name]=(a.copy(),b.copy());g[name]=(Vector((0,0,a.z)),Vector((0,0,b.z)))
 for side,sign,up in [('l',1,'L'),('r',-1,'R')]:
  sx=lambda n:src[n+'.'+up]
  s['upper_arm_'+side]=(sx('upperarm01')[0],sx('upperarm02')[1]);s['forearm_'+side]=(sx('lowerarm01')[0],sx('lowerarm02')[1]);s['hand_'+side]=(sx('wrist')[0],sx('finger3-1')[0]);s['clavicle_'+side]=(s['spine_03'][1].copy(),s['upper_arm_'+side][0].copy());armhead=s['upper_arm_'+side][0].copy();armhead.y=0;g['clavicle_'+side]=(g['spine_03'][1].copy(),armhead)
  u=Vector((sign,0,-1)).normalized();start=g['clavicle_'+side][1].copy()
  for name in ['upper_arm','forearm','hand']:
   a,b=s[name+'_'+side];end=start+u*(b-a).length;g[name+'_'+side]=(start.copy(),end.copy());start=end
  long=s['hand_'+side][1]-s['hand_'+side][0];radial=sx('finger2-1')[0]-sx('finger5-1')[0];palm=-sign*long.cross(radial).normalized()
  normals['forearm_'+side]=palm;normals['hand_'+side]=palm
  handsrc=frame(*s['hand_'+side],palm);handtarget=frame(*g['hand_'+side]);transform=handtarget@handsrc.inverted()
  for num,digit in enumerate(['thumb','index','middle','ring','little'],1):
   start=transform@sx(f'finger{num}-1')[0];direction=Vector((sign,0,0)) if num==1 else u
   for i in range(1,4):
    name=f'{digit}_{i:02}_{side}';a,b=sx(f'finger{num}-{i}');s[name]=(a,b);normals[name]=palm;end=start+direction*(b-a).length;g[name]=(start.copy(),end.copy());start=end
  s['thigh_'+side]=(sx('upperleg01')[0],sx('upperleg02')[1]);s['shin_'+side]=(sx('lowerleg01')[0],sx('lowerleg02')[1]);s['foot_'+side]=(sx('foot')[0],sx('toe3-1')[0]);s['toe_'+side]=(sx('toe3-1')[0],sx('toe3-3')[1])
  hip=s['thigh_'+side][0].copy();hip.x=sign*.098;hip.y=0;hip.z=s['thigh_'+side][0].z
  knee=hip+Vector((0,0,-(s['thigh_'+side][1]-s['thigh_'+side][0]).length));ankle=knee+Vector((0,0,-(s['shin_'+side][1]-s['shin_'+side][0]).length));g['thigh_'+side]=(hip,knee);g['shin_'+side]=(knee,ankle)
  offset=ankle-s['foot_'+side][0];g['foot_'+side]=(ankle,s['foot_'+side][1]+offset);toestart=g['foot_'+side][1];toelen=(s['toe_'+side][1]-s['toe_'+side][0]).length;g['toe_'+side]=(toestart,toestart+Vector((0,toelen,0)))
 names=[b['name'] for b in SK['bones'] if b['deform']];weights=np.zeros((len(xyz),len(names)));lookup={name:i for i,name in enumerate(names)};adapt={}
 for name,entries in json.loads((REF/'default_weights.mhw').read_text())['weights'].items():
  target=weight_map(name);adapt[name]=target
  for index,value in entries:weights[index,lookup[target]]+=value
 weights=weights[ids];weights/=weights.sum(axis=1)[:,None]
 points=np.zeros((len(ids),3));raw=xyz[ids]
 for k,n in enumerate(names):
  bindname=('foot_'+n[-1]) if n.startswith('toe_') else n
  mat=np.array(frame(*g[bindname])@frame(*s[bindname],normals.get(bindname,(0,1,0))).inverted());transformed=raw@mat[:3,:3].T+mat[:3,3];points+=transformed*weights[:,k,None]
 # Same rigid stature normalization applied to mesh and target bones after reposing splayed legs.
 low=points[:,2].min();high=points[:,2].max();scale=1.75/(high-low);points[:,2]-=low;points*=scale
 for name,(a,b) in g.items():
  if name=='root':continue
  offset=Vector((0,0,low));g[name]=((a-offset)*scale,(b-offset)*scale)
 return points,faces,g,names,weights,adapt,ids
