"""Isolated mannequin study paths; never redirect master builders."""
from pathlib import Path
R=Path(__file__).resolve().parents[2];ID='168h_human_anatomical_mannequin';RID='168h_rig_mannequin_v1';MASTER=R/'assets/humans/models'/ID;A=MASTER/'prototypes/v0.3.0';SOURCE=A/(ID+'.blend');RA=R/'assets/humans/rigs'/RID/'prototypes/v0.3.0';RSOURCE=RA/(RID+'.blend');F=R/'scenes/templates/168h_template_mannequin_anatomy_study';FS=F/(F.name+'.blend')
