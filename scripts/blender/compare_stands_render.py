"""Approved stands-local RGBA8 comparison; all other views remain exact."""
import numpy as np

def compare(reference, actual, limits=None):
    if reference.shape!=actual.shape or reference.ndim!=3 or reference.shape[2]!=4:
        return {'result':'FAIL','reason':'RGBA dimensions differ'}
    difference=np.abs(reference.astype(np.int16)-actual.astype(np.int16))
    maximum=int(difference.max());fraction=float(np.count_nonzero(difference)/difference.size)
    pixels=float(np.any(difference!=0,axis=2).mean());mean=float(difference.mean())
    alpha=bool(np.all(difference[:,:,3]==0))
    exact=maximum==0
    ok=exact if limits is None else (
        maximum<=limits['max_rgb_8bit_delta'] and alpha
        and fraction<limits['changed_rgba_channel_fraction_lt']
        and pixels<limits['changed_pixel_fraction_lt']
        and mean<=limits['mean_absolute_rgba_8bit_delta_lte'])
    return {'result':'PASS' if ok else 'FAIL','comparison':'exact' if limits is None else 'approved_stands_assembly_exception',
            'max_channel_delta':maximum/255,'max_8bit_delta':maximum,'changed_channel_fraction':fraction,
            'changed_channels':int(np.count_nonzero(difference)),'changed_pixel_fraction':pixels,
            'mean_absolute_8bit_delta':mean,'alpha_exact':alpha,'pixel_exact':exact}
