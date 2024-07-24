clear
close all
clc

% MCMC = readtable('MCMC_setup_info.xlsx');
variables    = ['Lv'];
chain_length = 500 % 4000;
% burn_in      = MCMC.burn_in_matlab(1);
num_params   = 1;
% num_mults    = MCMC.num_covmult(1);
upbound      = 9.00;
lobound      = 8.00';
num_chains   = 1;
% active_vars  = MCMC.active_vars';

% active_vars  = active_vars(~isnan(active_vars));
% variables    = variables(active_vars);
% upbound      = upbound(active_vars);
% lobound      = lobound(active_vars);
total_vars   = num_params % num_params+num_mults;

% for i =1:num_mults
%     upbound(end+1) = 2;
%     lobound(end+1) = 0;
%     variables(end+1) = {['$$m_' num2str(i) '$$']};
% end

% start_pts = importdata('outputs/start_pts.txt');
MAPs  = importdata('outputs/MAPs.txt');



%% fill in zeros for failed chains
failed_chains = importdata('outputs/failed_chains.txt');

if ~isempty(failed_chains)
    
    foo = zeros(num_chains, total_vars);
    
    
    c=0;
    for i = 1:num_chains
        
        if ~ismember(i,failed_chains)
            
            c=c+1;
            foo(i,:) = MAPs(c,:);
        end
    end
    
    
     MAPs = foo;
end



%% run the bash script to get info for evidence calculation 

% system(['bash get_info.sh  ' num2str(num_chains)  '  ' num2str(total_vars)  ]);



%% plot individual chains
combined_samples = [];
[sp1,sp2] = numSubplots(total_vars);
for j = setdiff(  1:num_chains,  failed_chains  ) % per chain

    file = [ 'outputs/case_' num2str(j+6) '_samples.txt'  ];
    samples = importdata(file);
    
    % samples(1:burn_in,:)=[];

    combined_samples = [combined_samples; samples];

    figure()

    for k = 1:total_vars
        
        subplot(sp1(1),sp1(2),k)
        histogram(samples(:,k),50,'edgecolor','none')
        xlim([ lobound(k)  upbound(k)  ]);
        xlabel(variables(k),'fontsize',20,'interpreter','latex');
        
        if k > num_params
            title([' MAP = ',num2str(MAPs(j,k))],'fontsize',20,'interpreter','latex')
        % else
        %     title(['Initial point = ',num2str(start_pts(j,k)),', MAP = ',num2str(MAPs(j,k))],'fontsize',20,'interpreter','latex')
        end

    end

    subtitle([ 'Case ' num2str(j+6) ]);
    set(gcf,'units','normalized','outerposition',[0 0 1 1])
    saveas(gcf,['figures/case_' num2str(j+6) '_histograms.png'])
    



%     fwd_mean = importdata([ 'outputs/chain_' num2str(j) '_fwd_mean.txt'  ]);
%     fwd_std  = importdata([ 'outputs/chain_' num2str(j) '_fwd_std.txt'  ]);

%     figure()
    
%         for i = 1:4 % split fwd into 4 curves
            
%             Ls = [250 500 1000 1500];

%         x = importdata(['reduced_Dc2/calibrationD' num2str(Ls(i)) 'nm_10pts.coords']);
        
        
        
%         y = fwd_mean(1:length(x))';
%         s =  fwd_std(1:length(x))';
%         fwd_mean(1:length(x))=[];
%         fwd_std(1:length(x))=[];

%         dy = importdata([ 'reduced_Dc2/calibrationD' num2str(Ls(i)) 'nm_10pts.1.dat']);
%         dv = importdata([ 'reduced_Dc2/calibrationD' num2str(Ls(i)) 'nm_10pts.1.sigma']);
%         ds = sqrt(dv);

%         shade(x,y,s,'r');hold on;
%         errorbar(x,dy,ds);
%         end
        
%         set(gca, 'fontsize',12);


% %         legend('Model','Data',...
% %                'location','northwest','fontsize',12,'interpreter','latex');
%         title([ 'Chain ' num2str(j) ],'fontsize',20,'interpreter','latex');
% %         xlim([0 13.2]);
%         xlabel('Strain ','fontsize',12,'interpreter','latex');
%         ylabel('Stress ','fontsize',12,'interpreter','latex');
%         pbaspect([4,3,1]);

    
%     set(gcf,'units','normalized','outerposition',[0 0 1 1])
%     saveas(gcf,['figures/chain_' num2str(j) '_fwd.png'])


end
    
    
% %% plot combined samples
% figure()

% means=[];
% stds=[];
% for k = 1:total_vars
%     subplot(sp1(1),sp1(2),k)
%     histogram(combined_samples(:,k),500,'edgecolor','none')
%     xlim([ lobound(k)  upbound(k)  ]);
%     xlabel(variables(k),'fontsize',20,'interpreter','latex');
    
    
    
%     if k > num_params
%         title([' Average MAP = ',num2str(mean(MAPs(:,k)))],'fontsize',20,'interpreter','latex');
%     else
%         title({[' Average MAP = ',num2str(mean(MAPs(:,k)))],...
%               ['$$\mu = $$' num2str(mean(combined_samples(:,k)))...
%               ', $$\sigma = $$' num2str(std(combined_samples(:,k)))]},'fontsize',20,'interpreter','latex')
%         means(end+1)=mean(combined_samples(:,k));
%         stds(end+1)=std(combined_samples(:,k));
%     end
    
% end
% suptitle([ 'All Chains Combined' ]);
% set(gcf,'units','normalized','outerposition',[0 0 1 1])
% saveas(gcf,['figures/combined_histograms.png'])



% save('combined_samples.txt','combined_samples', '-ascii');

% save('calibration_means.txt', 'means', '-ascii');
% save('calibration_stds.txt', 'stds', '-ascii');




%% generate histogram_bin_uncertain inputs for validation
figure()
for k = 1:num_params
    
    edges = linspace(lobound(k), upbound(k), 201);
    
    [N,~] = histcounts(combined_samples(:,k),edges);
    
    % assign 1 to bins with zero count to be compatible with dakota
    N(N==0)=1;
    
    
    
    
    subplot(sp1(1),sp1(2),k)
    histogram('BinEdges',edges,'BinCounts',N,'edgecolor','none')
    xlim([ lobound(k)  upbound(k)  ]);
    xlabel(variables(k),'fontsize',20,'interpreter','latex');
    
    
    % extend N with an redundant 0 to be compatible with dakota
    N(end+1)=0;
    
    save(['outputs/counts_' num2str(k) '.txt'],'N','-ascii');
    save(['outputs/edges_'  num2str(k) '.txt'],'edges','-ascii');
    
    
end
subtitle([ 'All Chains Combined - Smoothened for histogram_bin_uncertain' ]);
set(gcf,'units','normalized','outerposition',[0 0 1 1])
saveas(gcf,['figures/combined_histograms_dakota.png'])





    
    
% %% plot combined forward
% fwd_mean_combined = importdata([ 'outputs/combined_fwd_mean.txt'  ]);
% fwd_std_combined  = importdata([ 'outputs/combined_fwd_std.txt'  ]);

% figure()

%     for i = 1:4 % split fwd into 4 curves

%         Ls = [250 500 1000 1500];


%         x = importdata(['reduced_Dc2/calibrationD' num2str(Ls(i)) 'nm_10pts.coords']);
%         y = fwd_mean_combined(1:length(x))';
%         s =  fwd_std_combined(1:length(x))';
%         fwd_mean_combined(1:length(x))=[];
%         fwd_std_combined(1:length(x))=[];

%         dy = importdata([ 'reduced_Dc2/calibrationD' num2str(Ls(i)) 'nm_10pts.1.dat']);
%         dv = importdata([ 'reduced_Dc2/calibrationD' num2str(Ls(i)) 'nm_10pts.1.sigma']);
%         ds = sqrt(dv);

%         shade(x,y,s,'r');hold on;
%         errorbar(x,dy,ds);

%     end

%     set(gca, 'fontsize',14);
%     legend('Model','Data',...
%           'location','northwest','fontsize',16,'interpreter','latex');
%     title([ 'All Chains Combined' ],'fontsize',20,'interpreter','latex');
% %     xlim([0 13.2]);
%     xlabel('Strain \%','fontsize',16,'interpreter','latex');
%     ylabel('Stress MPa','fontsize',16,'interpreter','latex');
%     pbaspect([4,3,1]);


%     set(gcf,'units','normalized','outerposition',[0 0 1 1])
%     saveas(gcf,['figures/combined_fwd.png'])
    

    
    
    
    
    
    
% %     set(gcf, 'Units', 'Inches', 'Position', [0, 0, 5.7, 5.7/4*3], 'PaperUnits', 'Inches', 'PaperSize', [5.7, 5.7/4*3])

% % 
% % print(gcf, 'figs_papers/fwd.png', '-dpng', '-r300');
% % 


%% utilities

function h=shade(x,y,s,color) % assume input column vector

h=fill( [x' fliplr(x')], [y'+s' fliplr(y'-s')],color,'facealpha',0.5,'edgecolor','none' ); hold on;

end



function [p,n]=numSubplots(n)
% function [p,n]=numSubplots(n)
%
% Purpose
% Calculate how many rows and columns of sub-plots are needed to
% neatly display n subplots. 
%
% Inputs
% n - the desired number of subplots.     
%  
% Outputs
% p - a vector length 2 defining the number of rows and number of
%     columns required to show n plots.     
% [ n - the current number of subplots. This output is used only by
%       this function for a recursive call.]
%
%
%
% Example: neatly lay out 13 sub-plots
% >> p=numSubplots(13)
% p = 
%     3   5
% for i=1:13; subplot(p(1),p(2),i), pcolor(rand(10)), end 
%
%
% Rob Campbell - January 2010
   
    
while isprime(n) && n>4 
    n=n+1;
end
p=factor(n);
if length(p)==1
    p=[1,p];
    return
end
while length(p)>2
    if length(p)>=4
        p(1)=p(1)*p(end-1);
        p(2)=p(2)*p(end);
        p(end-1:end)=[];
    else
        p(1)=p(1)*p(2);
        p(2)=[];
    end    
    p=sort(p);
end
%Reformat if the column/row ratio is too large: we want a roughly
%square design 
while p(2)/p(1)>2.5
    N=n+1;
    [p,n]=numSubplots(N); %Recursive!
end
end
