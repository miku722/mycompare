PYTHON = python3

EVAL_DIR = $(shell pwd)
ROOT_DIR = $(EVAL_DIR)/../../
SOFT_SIM_DIR	= /home/kevin/projs/github/ara/
STORY_EVAL_DIR = $(EVAL_DIR)/tinystories
DRAW_DIR = $(EVAL_DIR)/visualization
TRACE_DIR = $(EVAL_DIR)/time_it_takes

update_testres:
	cat $(ROOT_DIR)/putty.log |grep "TEST FOR THE CHANGE OF RNG_SEED" -n
	sed -n '1036,$p' $(ROOT_DIR)/putty.log > $(STORY_EVAL_DIR)/test_res.txt

eval_q_nq:
	$(PYTHON) -m infer_Q_NQ_compare.main --input_file infer_Q_NQ_compare/test_res.txt

eval_story:
	$(PYTHON) -m tinystories.main --input_file tinystories/test_res.txt --output_file story_output.csv --offline True

eval_story_ollama:
	cd $(STORY_EVAL_DIR) && $(PYTHON) eval_ollama.py --input_file test_res.txt --output_file $(EVAL_DIR)/story_output.csv

eval_ulp:
	$(PYTHON) ulp_eval/evaluate.py --file_path /home/kevin/projs/github/ara/hardware/build/sim_gk.log

draw_q_nq:
	cd $(DRAW_DIR) && $(PYTHON) 160K_and_15M_quantization_compare_broken_axis.py

draw_accuracy:
	cd $(DRAW_DIR) && $(PYTHON) accuracy_compare.py --input_file ../story_output.csv.bak

draw_speed:
	cd $(DRAW_DIR) && $(PYTHON) token_per_second_compare.py

# trace function, and calcuilate the time 
DUMP_FILE  ?= llama2c260K_15M
FUNCT_NAME ?= matmul_Q_VIFMM
trace_funt:
	cd $(TRACE_DIR) && $(PYTHON) compare.py --input_dump_file $(SOFT_SIM_DIR)/app/bin/$(DUMP_FILE).dump --input_trace_file $(SOFT_SIM_DIR)/app/hardware/build/sim_gk.log --function_name 

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +

# rm -rf $(DRAW_DIR)/*.csv