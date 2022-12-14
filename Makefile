ifuncTool: function.c
	./ifuncCreator function.c compile

ifuncTool_noCompile: function.c
	./ifuncCreator function.c

testSIMD: 
	./ifuncMain tests/input/bree.jpg 1.0 1.0 1.0 tests/output/bree1a.jpg
	./ifuncMain tests/input/bree.jpg 0.5 0.5 0.5 tests/output/bree2a.jpg
	./ifuncMain tests/input/bree.jpg 2.0 2.0 2.0 tests/output/bree3a.jpg

testSVE2:
	qemu-aarch64 ./ifuncMain tests/input/bree.jpg 1.0 1.0 1.0 tests/output/bree1b.jpg
	qemu-aarch64 ./ifuncMain tests/input/bree.jpg 0.5 0.5 0.5 tests/output/bree2b.jpg
	qemu-aarch64 ./ifuncMain tests/input/bree.jpg 2.0 2.0 2.0 tests/output/bree3b.jpg

clean:
	rm tests/output/bree??.jpg

