clc; clear all; close all; 
load('shoesducks.mat');
%% Splitting data into training and test outputs

trainingInput = X(1:72,:);
trainingOutput = Y(1:72,:);
testInput = X(73:144,:);
testOutput = Y(73:144,:);

%% Support Vector Classification (Linear Kernel)

[nsv_lin, alpha_lin, bias_lin] = svc(trainingInput, trainingOutput);
tstY_lin = svroutput(trainingInput, testInput, 'linear', alpha_lin, bias_lin);
err_lin = svrerror(trainingInput, testInput, testOutput,'linear',alpha_lin,bias_lin)

%% Support Vector Classification (Polynomial Kernel)
global p1 %p1 represents degree of polynomial
err_poly = []
for a=1:1:5
    p1 = a;
    [nsv_poly, alpha_poly, bias_poly] = svc(trainingInput, trainingOutput);
    tstY_poly = svroutput(trainingInput, testInput, 'poly', alpha_poly, bias_poly);
    err_poly = [err_poly svrerror(trainingInput, testInput, testOutput,'poly',alpha_poly,bias_poly)]
end
%% Support Vector Classification (rbf Kernel)
global p1 %p1 represents standard deviation
err_rbf = []
for a=1:1:5
    p1 = a;
    [nsv_rbf, alpha_rbf, bias_rbf] = svc(trainingInput, trainingOutput);
    tstY_rbf = svroutput(trainingInput, testInput, 'rbf', alpha_rbf, bias_rbf);
    err_rbf = [err_rbf svrerror(trainingInput, testInput, testOutput,'rbf',alpha_rbf,bias_rbf)]
end

figure;
plot(err_poly);
title('Error of Polynomial Kernel');
xlabel('Order of polynomial');
ylabel('Error');
grid on
figure;
plot(err_rbf);
title('Error of RBF Kernel');
xlabel('Standard deviation');
ylabel('Error');