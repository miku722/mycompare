EVAL_DIR = $(shell pwd)
ROOT_DIR = $(EVAL_DIR)/../../
STORY_EVAL_DIR = $(EVAL_DIR)/tinystories

update_testres:
	cat $(ROOT_DIR)/putty.log |grep "TEST FOR THE CHANGE OF RNG_SEED" -n
	sed -n '1036,$p' $(ROOT_DIR)/putty.log > $(STORY_EVAL_DIR)/test_res.txt

eval_q_nq:
	python -m infer_Q_NQ_compare.main --input_file infer_Q_NQ_compare/test_res.txt 

eval_story:
	python -m tinystories.main --input_file tinystories/test_res.txt --output_file story_output.csv --offline False

eval_ulp:
	python ulp_eval/evaluate.py --file_path /home/kevin/projs/ara/hardware/build/sim_gk.log

draw_q_nq:
	cd visualization && python 160K_and_15M_quantization_compare_broken_axis.py

draw_accuracy: 
	cd visualization && python accuracy_compare.py

draw_speed: 
	cd visualization && python token_per_second_compare.py

clean:
	rm -rf $(STORY_EVAL_DIR)/story_output.csv