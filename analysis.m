% Matlab Analysis
a=importdata('titles')
b=importdata('titles2')

subplot(2,1,1)
title('Science / Nature')
hist(log10(a(:,1)),0:0.2:4)
ylabel('Count')
subplot(2,1,2)
title('PloS One')
hist(log10(b(:,1)),0:0.2:4)
xlabel('Log10(citations)')


subplot(2,1,1)
hist(a(:,2),0:1:30)
title('Science / Nature')
ylabel('Count')
subplot(2,1,2)
hist(b(:,2),0:1:30)
title('PloS One')
xlabel('Words in title')
ylabel('Count')
