% Matlab Script to detect lines on an image

function image = lineDect(args)
	% load in image
	readimage = args.arg1
	saveimage = args.arg2
	original = imread (readimage);

	% convert to greyscale (notice spelling :( )
	grayscale = rgb2gray(original);

	% adjust contrast to darken the image, 
	contrast = imadjust(grayscale,[0.3 0.6], []);

	% create the gaussian filter with hsize = [5 5] and sigma = 2
	G = fspecial('gaussian',[13 13],3);

	% filter it to blur the image, and display
	blurContrast = imfilter(contrast,G,'same');

	% edge detection on blurred increased contrast image 
	cannyDetection = edge (blurContrast, 'canny', [0.15, 0.3]);

	imwrite(cannyDetection, saveimage);
end






