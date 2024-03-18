clear 
close all
clc



% MCMC = readtable('MCMC_setup_info.xlsx');
% variables    = MCMC.matlab_vars_tag';
chain_length = 500 % 4000;
% burn_in      = MCMC.burn_in_matlab(1);
num_params   = 1;
% num_mults    = MCMC.num_covmult(1);
% upbound      = MCMC.upper_bounds';
% lobound      = MCMC.lower_bounds';
num_chains   = 1;
total_vars   = num_params; % num_params+num_mults;

failed_chains = [];


MAPs = [];
% combined_fwd=[];
for j = 1:num_chains    

    file = [ 'case_' num2str(j+6) '/dakota_mcmc_tabular.dat'  ];
    
    if isfile(file)

        Samples = importdata(file);

        data = Samples.data(:,1:total_vars);

        save(['outputs/case_' num2str(j+6) '_samples.txt'],  'data', '-ascii');

        % fwd = Samples.data(burn_in+1:end, (total_vars+1):end  );
        
        % fwd_mean = mean(fwd);
        % fwd_std  =  std(fwd);
        
        % combined_fwd = [ combined_fwd; fwd];


        % save([ 'outputs/case_' num2str(j+3) '_fwd_mean.txt'  ],  'fwd_mean', '-ascii');
        % save([ 'outputs/case_' num2str(j+3) '_fwd_std.txt'  ],  'fwd_std', '-ascii');
        
        
        % read in MAPs
        MAPs = [ MAPs;  findmap( ['case_' num2str(j+6) '/QuesoDiagnostics'],  total_vars ) ];
        
        
        
    else
        disp(['Warning: Case #' num2str(j+6) ' failed!...']);
        failed_chains(end+1) = j;
    end

end

% fwd_mean_combined = mean(combined_fwd);
% fwd_std_combined  =  std(combined_fwd);


% save([ 'outputs/combined_fwd_mean.txt'  ],  'fwd_mean_combined', '-ascii');
% save([ 'outputs/combined_fwd_std.txt'  ],  'fwd_std_combined', '-ascii');
save([ 'outputs/failed_chains.txt'  ],  'failed_chains', '-ascii');
save([ 'outputs/MAPs.txt'  ],  'MAPs', '-ascii');

MAPs

%% 

function x = findmap(dir, numvars)

textbylines = regexp( fileread( [dir '/display_sub0.txt'] ) ,'\n','split');

whichline = find(  contains(textbylines,  'rawUnifiedMAPpositions')  );

theline = char(textbylines(whichline));

brokenline = strsplit(theline, {' ','\n','\b'});

numerics = str2double(brokenline);
numerics=numerics(~isnan(numerics));


x = numerics(end+1-numvars:end);



end





    