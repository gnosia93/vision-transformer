from typing import Optional, Tuple
import torch 
import torch.nn as nn

class SiglipVisionConfig:
    def __init__(self, hidden_size=768, 
                 intermediate_size=3072, 
                 num_hidden_layers=12,
                 num_attention_heads=12,
                 num_channels=3,
                 image_size=224,
                 patch_size=16,             # pach_size means 16x16 pixels
                 layer_norm_eps=1e-6,
                 attention_dorpout=0.0,
                 num_image_tokens: int = None,
                 **kwargs):
        super().__init__()
        
        self.hideen_size = hidden_size
        self.intermediate_size = intermediate_size
        self.num_hidden_layers = num_hidden_layers
        self.num_attention_heads = num_attention_heads
        self.num_channels = num_channels
        self.patch_size = patch_size
        self.image_size = image_size
        self.attention_dropout = attention_dorpout
        self.layer_norm_eps = layer_norm_eps
        self.num_image_tokens = num_image_tokens 


class SiglipVisionEmbeddings(nn.Module):
    def __init__(self, config: SiglipVisionConfig):
        super().__init__()
        self.config = config 
        self.embed_dim = config.hideen_size
        self.image_size = config.image_size 
        self.patch_size = config.patch_size 

        self.patch_embedding = nn.Conv2d(
            in_channels=config.num_channels,
            out_channels=self.embed_dim,
            kernel_size=self.patch_size, 
            stride=self.patch_size,
            padding="valid"
        )

        self.num_patches = (self.image_size // self.patch_size) ** 2
        self.num_positions = self.num_patches 
        self.position_embedding = nn.Embedding(self.num_positions, self.embed_dim)
        self.register_buffer(
            "position_ids",
            torch.arange(self.num_positions).expand((1, -1)),
            persistent=False,
        )

    def forward(self, pixel_values: torch.FloatTensor) -> torch.Tensor:
        pass 
    

class SiglipVisionTransformer(nn.Module):
    def __init__(self, config:SiglipVisionConfig):
        super().__init__()
        self.config = config 
        embed_dim = config.hideen_size

        self.embeddings = SiglipVisionEmbeddings(config)
        self.encoder = SiglipEncoder(config)
        self.post_layernorm = nn.LayerNorm(embed_dim, eps=config.layer_norm_eps)

    def forward(self, pixel_values: torch.Tensor) -> torch.Tensor:
        # pixel_values: batch_size, channels, height, width -> batch_size, num_patches, embed_dim
        hiden_states = self.embeddings(pixel_values)
        last_hidden_state = self.encoder(inputs_embeds=hiden_states)
        last_hidden_state = self.post_layernorm(last_hidden_state)
        return last_hidden_state


class SiglipVisionModel(nn.Module):

    def __init__(self, config: SiglipVisionConfig):
        super().__init__()
        self.config = config 
        self.vision_model = SiglipVisionTransformer(config) 
    
    def forward(self, pixel_values) -> Tuple: 
        # batch_size, channels, height, width -> batch_size, num_patches, embed_dim
        return self.vision_model(pixel_values)