import sys
sys.path.insert(0, ".")
import html
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_DIR = "models/nli-deberta-v3-finetuned"
tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
model.eval()

def generate_neural_heatmap_html(text, token_weights):
    if not token_weights:
        return html.escape(text)
    
    # Sort by start offset
    token_weights = sorted(token_weights, key=lambda x: x[0][0])
    
    # Min-max normalize across these weights
    weights = [w for _, w in token_weights]
    min_w, max_w = min(weights), max(weights)
    
    html_parts = []
    curr_idx = 0
    for (start, end), w in token_weights:
        if start > curr_idx:
            html_parts.append(html.escape(text[curr_idx:start]))
        
        norm_w = (w - min_w) / (max_w - min_w + 1e-8)
        # Scale alpha between 0.08 and 0.70
        alpha = round(0.08 + 0.62 * (norm_w ** 1.5), 3) if norm_w > 0.15 else 0.0
        tok_text = html.escape(text[start:end])
        if alpha > 0.05:
            html_parts.append(f'<span class="xai-token" data-weight="{norm_w:.3f}" style="background-color: rgba(239, 68, 68, {alpha}); padding: 1px 2px; border-radius: 2px;" title="Attention: {norm_w:.3f}">{tok_text}</span>')
        else:
            html_parts.append(tok_text)
        curr_idx = end
        
    if curr_idx < len(text):
        html_parts.append(html.escape(text[curr_idx:]))
        
    return "".join(html_parts)

premise = "Section 195. Protest of Assessment. The taxpayer may file a written protest without being required to pay the assessment under protest."
hypo = "Section 423. Payment Under Protest. No protest against an assessment shall be entertained unless the taxpayer first pays under protest the tax assessed."

inputs = tokenizer(premise, hypo, return_offsets_mapping=True, return_tensors="pt", truncation=True, max_length=512)
with torch.no_grad():
    outputs = model(input_ids=inputs["input_ids"], attention_mask=inputs["attention_mask"], output_attentions=True)
    probs = F.softmax(outputs.logits, dim=-1)[0]
    attentions = outputs.attentions

cls_attn = attentions[-1][0].mean(dim=0)[0].cpu().numpy()
offsets = inputs["offset_mapping"][0].tolist()
seq_ids = inputs.sequence_ids(0)

prem_tok_w = []
hypo_tok_w = []
for s_id, off, w in zip(seq_ids, offsets, cls_attn):
    if s_id == 0 and off != [0, 0]:
        prem_tok_w.append((off, float(w)))
    elif s_id == 1 and off != [0, 0]:
        hypo_tok_w.append((off, float(w)))

prem_html = generate_neural_heatmap_html(premise, prem_tok_w)
hypo_html = generate_neural_heatmap_html(hypo, hypo_tok_w)

print("PREMISE HTML:")
print(prem_html)
print("\nHYPOTHESIS HTML:")
print(hypo_html)
