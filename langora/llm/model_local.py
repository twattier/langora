from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from transformers import GenerationConfig, pipeline
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
import torch

from .model import Model
from config.env import Config

class ModelLocal(Model):
    def __init__(self) -> None:
        Model.__init__(self)
        self.device = "cpu"

    def init_model(self):        
        if self.llm:
            return

        print("Load Tokenizer : " + Config.MODEL_TOKEN)
        tokenizer = AutoTokenizer.from_pretrained(Config.MODEL_TOKEN, 
                                                       cache_dir=Config.HUGGINGFACE_CACHE, 
                                                       trust_remote_code=True
                                                       )
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.padding_side = "right"
        
        if not torch.cuda.is_available():
            print("Load Model : " + Config.MODEL_GEN + " [CPU]")
            model = AutoModelForCausalLM.from_pretrained(Config.MODEL_GEN, cache_dir=Config.HUGGINGFACE_CACHE)            
        else:
            print("Load Model : " + Config.MODEL_GEN + " [CUDA]")        
            torch.cuda.empty_cache()
           
            # use_4bit = True                     # Activate 4-bit precision base model loading            
            # bnb_4bit_compute_dtype = "float16"  # Compute dtype for 4-bit base models            
            # bnb_4bit_quant_type = "nf4"         # Quantization type (fp4 or nf4)
            # # Activate nested quantization for 4-bit base models (double quantization)
            # use_nested_quant = False            
            # compute_dtype = getattr(torch, bnb_4bit_compute_dtype)
            # bnb_config = BitsAndBytesConfig(
            #     load_in_4bit=use_4bit,
            #     bnb_4bit_quant_type=bnb_4bit_quant_type,
            #     bnb_4bit_compute_dtype=compute_dtype,
            #     bnb_4bit_use_double_quant=use_nested_quant,
            # )
            # # Check GPU compatibility with bfloat16
            # if compute_dtype == torch.float16 and use_4bit:
            #     major, _ = torch.cuda.get_device_capability()
            #     if major >= 8:
            #         print("=" * 80)
            #         print("Your GPU supports bfloat16: accelerate training with bf16=True")
            #         print("=" * 80)

            quantization_config = BitsAndBytesConfig(llm_int8_enable_fp32_cpu_offload=True)
            model = AutoModelForCausalLM.from_pretrained(
                Config.MODEL_GEN,
                cache_dir=Config.HUGGINGFACE_CACHE,
                # quantization_config=bnb_config,
                device_map="auto",            
                quantization_config=quantization_config,
                load_in_8bit=True,            
            )
            self.device = "cuda"
        size = model.get_memory_footprint()/(1024**3)
        print(f"Model loaded : {size:.1f}GB")

        generation_config = GenerationConfig.from_pretrained(Config.MODEL_GEN)
        generation_config.max_new_tokens = 1024
        generation_config.temperature = 0.0001
        generation_config.top_p = 0.95
        generation_config.do_sample = True
        generation_config.repetition_penalty = 1.15

        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            return_full_text=True,
            generation_config=generation_config,
        )
        self.llm = HuggingFacePipeline(pipeline=pipe)