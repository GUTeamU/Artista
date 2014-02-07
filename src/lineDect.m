% Matlab Script to detect lines on an image
clf

% load in image
original = imread ('fraser.jpg');
figure('name', 'original image'), imshow(original)

% convert to greyscale (notice spelling :( )
grayscale = rgb2gray(original);
figure('name', 'grayscale image'), imshow(grayscale)

% adjust contrast to darken the image, 
contrast = imadjust(grayscale,[0.3 0.6], []);
figure('name', 'darkened image'), imshow(contrast)

% create the gaussian filter with hsize = [5 5] and sigma = 2
G = fspecial('gaussian',[13 13],3);

% filter it to blur the image, and display
blurContrast = imfilter(contrast,G,'same');
figure('name', 'darkened image with Gaussian blur filter'), imshow(blurContrast)

% edge detection on blurred increased contrast image 
cannyDetection = edge (blurContrast, 'canny', [0.15, 0.3]);
figure('name', 'canny line detection on image'), imshow(cannyDetection)

% wiener filter to gel lines together
wiener = wiener2(cannyDetection, [3 3]);
figure('name', 'wiener filter gels dots into ticker lines'), imshow(wiener)
imwrite(wiener, '/users/level3/1102103l/University/matlab/wiener.jpg');







