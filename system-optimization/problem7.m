% Problem 10.15a
% clc; clear all; close all;
% iterations = 100;
% alpha = 0.01;
% beta = 0.5;
% error = 1e-7;
% xval = [];
% n = 100;
% p = 30;
% x = rand(n,1);
% A = rand(p,n);
% xval = [];
% for i=1:iterations
%    value = x'*log(x);
%    gradient = 1 + log(x);
%    hessianian = diag(1./x);
%    solution = -[hessianian A';A zeros(p,p)]\[gradient; zeros(p,1)];
%    v = solution(1:n);
%    f_prime = gradient'*v;
%    xval = [xval error-f_prime];
%    if abs(f_prime) < error
%        k = i;
%        break;
%    end
%    t = 1;
%    while min(x+t*v) <= 0
%        t = beta * t;
%    end
%    while ((x+t*v)'*log(x+t*v)) >= value + t*alpha*f_prime
%        t = beta * t;
%    end
%    x = x + t*v;
% end
% 
% plot([1:length(xval)], xval)
% 
% 
% Problem 10.15b
% 
% iterations = 100;
% alpha = 0.01;
% beta = 0.5;
% error = 1e-7;
% p = 30;
% n = 100;
% A = rand(p,n);
% x0 = ones(n,1);
% x1 = rand(n,1);
% x = x0;
% y = x1;
% nu=zeros(p,1);
% resdls = [];
% for i=1:iterations
%     r = [1+log(x)+A'*nu; A*x-b]; 
%     resdls = [resdls, norm(r)];
%     sol = -[diag(1./x) A'; A zeros(p,p)] \ r;
%     Dx = sol(1:n); Dnu = sol(n+[1:p]);
%     if (norm(r) < error), break; end
%         t=1;
%     while (min(x+t*Dx) <= 0) 
%         t = beta*t; 
%     end
%     while norm([1+log(x+t*Dx)+A'*(nu+Dnu); A*(x+Dx)-b]) > (1-alpha*t)*norm(r)
%         t = beta*t
%     end
%     x = x + t*Dx; 
%     nu = nu + t*Dnu;
% end

% Problem 10.15 c
p = 30;
n = 100;
iterations = 100;
alpha = 0.01;
beta = 0.5;
error = 1e-8;
x = rand(n,1);
A = rand(p,n);
b = A*x;
fp = [];
nu = zeros(p,1);
for i=1:iterations
    val = b'*nu + sum(exp(-A'*nu-1));
    grad = b - A*exp(-A'*nu-1);
    hessian = A*diag(exp(-A'*nu-1))*A';
    v = -hessian\grad;
    fprime = grad'*v;
    display(fprime);
    if (abs(fprime) < error)
        display(i);
        break; 
    end
    t=1;
    while (b'*(nu+t*v) + sum(exp(-A'*(nu+t*v)-1)) > val + t*alpha*fprime)
        t = beta*t;
    end
    fp = [fp fprime];
    nu = nu + t * v;
end
