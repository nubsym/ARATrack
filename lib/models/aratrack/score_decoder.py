"""
SPM: Score Prediction Module
"""
import torch
import torch.nn as nn
from einops import rearrange
from lib.models.aratrack.head import MLP
from external.PreciseRoIPooling.pytorch.prroi_pool import PrRoIPool2D

class ScoreDecoder(nn.Module):
    def __init__(self, num_heads=12, hidden_dim=768, nlayer_head=3, pool_size=4):
        super().__init__()
        self.pool_size = pool_size
        self.score_head = MLP(hidden_dim, hidden_dim, 1, nlayer_head)
        self.search_prroipool = PrRoIPool2D(pool_size, pool_size, spatial_scale=1.0)

        self.avgpool = nn.AdaptiveAvgPool1d(1)

    def forward(self, search_feat, search_box):
        """
        :param search_box: with normalized coords. (x0, y0, x1, y1)
        :return:
        """
        b, c, h, w = search_feat.shape
        search_box = search_box.clone() * w
        bb_pool = search_box.view(-1, 4)
        # Add batch_index to rois
        batch_size = bb_pool.shape[0]
        batch_index = torch.arange(batch_size, dtype=torch.float32).view(-1, 1).to(bb_pool.device)
        target_roi = torch.cat((batch_index, bb_pool), dim=1)

        search_box_feat = rearrange(self.search_prroipool(search_feat, target_roi), 'b c h w -> b (h w) c')
        search_box_feat = self.avgpool(search_box_feat.transpose(-1, -2)).transpose(-1, -2)
        out_scores = self.score_head(search_box_feat)

        return out_scores
