function as8(M,r,c)
    result = M(r-1,c-1) + M(r-1,c) + M(r-1,c+1) + ...
             M(r,c-1)   + M(r,c+1) + M(r+1,c-1) + ...
                          M(r+1,c) + M(r+1,c+1);
    result = result / 8;
    return result;
end