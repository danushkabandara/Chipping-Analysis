I = imread('chip4.jpg');
I = rgb2gray(I);
[~,threshold] = edge(I,'sobel');
BWs = edge(I,'sobel',threshold *1.5);
se90 = strel('line',3,90);
se0 = strel('line',3,0);
BWsdil = imdilate(BWs,[se90 se0]);
BWdfill = imfill(BWsdil,'holes');
BW2 = bwareafilt(BWdfill,3);

[rows,col]=find(BW2);
row_median=median(rows);


detected_size = [];
for K = 1 : size(BW2,2)
  thiscolumn = BW2(:,K,:);
  crop = thiscolumn(1:150,:) %get only the top part of column to prevent artifacts at bottom from affecting the analysis
  last_non_zero_row_pos = find(crop,1,'last');% last non zero element
  detected_size = [detected_size; (last_non_zero_row_pos)];
 % plot(K, last_non_zero_row_pos, 'y*', 'LineWidth', 1, 'MarkerSize', 1);
  %plot(K, row_median, 'b*', 'LineWidth', 1, 'MarkerSize', 1);
end
[pks,locs] = findpeaks(detected_size,[1:size(BW2,2)],'MinPeakDistance',6);
imshow(BW2)
hold on;

for L = 1 : size(locs,2)
    plot(locs(L), pks(L),'r*', 'LineWidth', 1, 'MarkerSize', 2);%plot peaks
end
