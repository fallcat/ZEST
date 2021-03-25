import torch
import torch.nn as nn

class Attention(nn.Module):
    def __init__(self, dimensions=3584,text_dim=7621):
        super(Attention, self).__init__()

        self.linear_out = nn.Linear(dimensions * 2, dimensions, bias=False)
        self.softmax = nn.Softmax(dim=-1)
        self.tanh = nn.Tanh()
        self.main = nn.Linear(text_dim, dimensions, bias=False)

    def forward(self, query, text_feat):

        context = self.main(text_feat)
        context = context.expand(query.shape[0], context.shape[1], context.shape[2])  # batch_size, num_classes, image_dim
        query = query.unsqueeze(1)
        batch_size, output_len, dimensions = query.size()  # output_len = 1?
        query_len = context.size(1)  # num_cls

        attention_scores = torch.bmm(query, context.transpose(1, 2).contiguous())
        # query (bsz, 1, img_dim) x context (bsz, img_dim, num_cls) = (bsz, 1, num_cls)

        attention_scores = attention_scores.view(batch_size * output_len, query_len)  # (bsz, num_cls)

        attention_weights = self.softmax(attention_scores)
        attention_weights = attention_weights.view(batch_size, output_len, query_len)  # (bsz, 1, num_cls)

        return attention_weights, attention_scores