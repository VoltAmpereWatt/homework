clc; clear all; close all;

alpha = 0.01;
beta = 0.5;
iterations = 1000;
tolerance = 1e-3;
m = 200;
n = 100;
A = rand(m,n);
x = zeros(n,1);
xvals =[];
for iter = 1:iterations
    val = -sum(log(1-A*x)) - sum(log(1+x)) - sum(log(1-x));
    grad = A'*(1./(1-A*x)) - 1./(1+x) + 1./(1-x);
    if norm(grad) < tolerance
        display(iter);
        break; 
    end;
    v = -grad;
    fprime = grad'*v;
    display(fprime);
    t = 1; 
    while ((max(A*(x+t*v)) >= 1) | (max(abs(x+t*v)) >= 1))
        t = beta*t;
    end;
    while (-sum(log(1-A*(x+t*v))) - sum(log(1-(x+t*v).^2)) > val + alpha*t*fprime)
        t = beta*t;
    end
    x = x+t*v;
    xvals = [xvals norm(grad)];
end;

alpha = 0.01;
beta = 0.5;
iterations = 1000;
error = 1e-8;
m = 200;
n = 100;
x = zeros(n,1);
A = rand(m,n);
xvals = [];
for iter = 1:iterations
    val = -sum(log(1-A*x)) - sum(log(1+x)) - sum(log(1-x));
    d = 1./(1-A*x);
    grad = A'*d - 1./(1+x) + 1./(1-x);
    hess = A'*diag(d.^2)*A + diag(1./(1+x).^2 + 1./(1-x).^2);
    v = -hess\grad;
    fprime = grad'*v;
    if abs(fprime) < error
        display(iter)
        break; 
    end;
    t = 1; 
    while ((max(A*(x+t*v)) >= 1) | (max(abs(x+t*v)) >= 1))
        t = beta*t;
    end;
    while ( -sum(log(1-A*(x+t*v))) - sum(log(1-(x+t*v).^2)) > val + alpha*t*fprime)
        t = beta*t;
    end;
    x = x+t*v;
    xvals = [xvals norm(grad)];
end;    