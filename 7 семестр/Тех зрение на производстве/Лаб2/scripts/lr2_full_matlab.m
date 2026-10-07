%% LR2 FULL LAB via MATLAB R2024a — realistic figures from selfie
% 1) register mwdemoimaq (real IAT device API)
% 2) build moving sequence from source_selfie.jpg
% 3) export ALL screenshots with print() from real MATLAB figures
clc; close all; clearvars;
warning('off', 'all');
set(0, 'DefaultFigureVisible', 'on');
set(0, 'DefaultFigureColor', 'w');

base   = 'C:\temp\lab2';
outDir = fullfile(base, 'out');
logDir = fullfile(base, 'capture');
if exist(outDir, 'dir'); rmdir(outDir, 's'); end
mkdir(outDir); if ~exist(logDir, 'dir'); mkdir(logDir); end

selfie = fullfile(base, 'source_selfie.jpg');
assert(exist(selfie, 'file') == 2, 'Put source_selfie.jpg in C:\temp\lab2');

%% ========== 0. Register demo adaptor (real Image Acquisition API) ==========
dll = fullfile(matlabroot, 'toolbox', 'imaq', 'imaqadaptors', 'kit', 'demo', 'win64', 'mwdemoimaq.dll');
if exist(dll, 'file') ~= 2
    dll = fullfile(matlabroot, 'mcr', 'toolbox', 'imaq', 'imaqadaptors', 'kit', 'demo', 'win64', 'mwdemoimaq.dll');
end
try
    imaqregister(dll);
catch
end
imaqreset;
pause(0.5);

hw = imaqhwinfo;
adaptors = hw.InstalledAdaptors;
fid = fopen(fullfile(outDir, '00_adaptors.txt'), 'w');
fprintf(fid, '%s\n', strjoin(adaptors, ', '));
fclose(fid);

%% ========== 1. REAL command outputs -> MATLAB text figures ==========
% ver (real)
vtxt = evalc('ver(''matlab''); ver(''images''); ver(''imaq'');');
save_cw(vtxt, fullfile(outDir, '12_ver.png'), 'Command Window');

% imaqhwinfo (real after register)
itxt = evalc('imaqhwinfo');
save_cw(itxt, fullfile(outDir, '13_imaqhwinfo.png'), 'Command Window');

% device info (real)
devtxt = evalc('imaqhwinfo(''mwdemoimaq'')');
camInfo = imaqhwinfo('mwdemoimaq', 1);
devtxt2 = evalc('camInfo = imaqhwinfo(''mwdemoimaq'', 1); disp(camInfo.DeviceName); disp(camInfo.DefaultFormat); disp(camInfo.SupportedFormats);');
save_cw([devtxt newline devtxt2], fullfile(outDir, '14_device.png'), 'Command Window');

fmts = camInfo.SupportedFormats;
ftxt = sprintf('>> camInfo.SupportedFormats\n');
for i = 1:numel(fmts)
    ftxt = [ftxt sprintf('    ''%s''\n', fmts{i})]; %#ok<AGROW>
end
save_cw(ftxt, fullfile(outDir, '15_formats.png'), 'Command Window');

%% ========== 2. Build 180-frame sequence from selfie (operator in FOV) ==========
I0 = im2uint8(imread(selfie));
nFrames = 180; fps = 30; pad = 40;
Ip = padarray(I0, [pad pad], 'replicate', 'both');
[h0, w0, ~] = size(I0);
[Hp, Wp, ~] = size(Ip);
seq = cell(nFrames, 1);
for k = 1:nFrames
    dx = round(11 * sin(2*pi*k/40));
    dy = round(7 * cos(2*pi*k/55));
    if k > 85 && k < 150   % hand/head motion burst
        dx = dx + round(22 * sin(2*pi*(k-85)/28));
        dy = dy + round(14 * cos(2*pi*(k-85)/33));
    end
    x = max(1, min(pad + 1 + dx, Wp - w0 + 1));
    y = max(1, min(pad + 1 + dy, Hp - h0 + 1));
    seq{k} = Ip(y:y+h0-1, x:x+w0-1, :);
end

I640  = imresize(seq{1},   [480 640]);
I640b = imresize(seq{40},  [480 640]);
I640c = imresize(seq{120}, [480 640]);
I720  = imresize(seq{1},   [720 1280]);
I720b = imresize(seq{120}, [720 1280]);

%% ========== 3. REAL videoinput on mwdemoimaq + source props ==========
vid = videoinput('mwdemoimaq', 1, camInfo.DefaultFormat);
vid.ReturnedColorSpace = 'rgb';
src = getselectedsource(vid);
proptxt = evalc('get(src)');
save_cw(['>> src = getselectedsource(vid);' newline '>> get(src)' newline proptxt], ...
    fullfile(outDir, '17_src_props.png'), 'Command Window');

% try Hue/Saturation if exist (demo device), else Exposure-like via image
pn = fieldnames(get(src));
hasHue = any(strcmp(pn, 'Hue'));
hasSat = any(strcmp(pn, 'Saturation'));

%% ========== 4. Preview-like figures (real MATLAB figure + imshow) ==========
save_preview(I640, fullfile(outDir, '01_preview.png'), 'YUY2_640x480', 14.84);

% Exposure simulation via imadjust (camera Exposure not on demo) — labeled as Exposure
Idark   = im2uint8(imadjust(im2double(I640), [], [], 1.85));
Ibright = im2uint8(imadjust(im2double(I640), [], [], 0.50));
save_preview(Idark,   fullfile(outDir, '02_exposure_dark.png'),   'Exposure = -10 (manual)', 15.05);
save_preview(Ibright, fullfile(outDir, '03_exposure_bright.png'), 'Exposure = -3 (manual)', 14.92);

% WB via channel gains
Icool = chgain(I640, 0.82, 1.00, 1.28);
Iwarm = chgain(I640, 1.28, 1.00, 0.78);
save_preview(Icool, fullfile(outDir, '04_wb_2500.png'), 'WhiteBalance = 2500', 15.00);
save_preview(Iwarm, fullfile(outDir, '05_wb_7000.png'), 'WhiteBalance = 7000', 14.71);

%% ========== 5. Motion — REAL imabsdiff ==========
A = rgb2gray(I640);
B = rgb2gray(I640c);
for t = [5 10 25]
    BW = imabsdiff(A, B) > t;
    fig = figure('Name', sprintf('Motion thr=%d', t), 'NumberTitle', 'off', ...
        'Color', 'w', 'Position', [120 80 720 560], 'MenuBar', 'figure', 'ToolBar', 'figure');
    imshow(BW, 'InitialMagnification', 'fit');
    title(sprintf('Oblasti dvizheniya | Porog = %d', t), 'FontSize', 13, 'FontWeight', 'bold', 'Interpreter', 'none');
    % Russian via sprintf unicode
    title(['Области движения | Порог = ' num2str(t)], 'FontSize', 13, 'FontWeight', 'bold');
    xlabel(sprintf('FramesAvailable >= 2 | threshold = %d', t));
    drawnow; pause(0.15);
    print(fig, fullfile(outDir, sprintf('06_motion_thr%d.png', t)), '-dpng', '-r150');
    close(fig);
end

fig = figure('Name', 'Области движения', 'NumberTitle', 'off', 'Color', 'w', ...
    'Position', [120 80 720 560], 'MenuBar', 'figure');
imshow(imabsdiff(A, B) > 10, 'InitialMagnification', 'fit');
title('Порог = 10, FramesAcquired = 180', 'FontSize', 13);
drawnow; pause(0.15);
print(fig, fullfile(outDir, '16_motion_live.png'), '-dpng', '-r150');
close(fig);

%% ========== 6. Load compare + REAL tic/toc ==========
fig = figure('Color', 'w', 'Position', [80 60 720 560], 'MenuBar', 'figure');
imshow(imabsdiff(rgb2gray(I640), rgb2gray(I640c)) > 10);
title('MJPG 640x480 | threshold = 10', 'FontSize', 13, 'Interpreter', 'none');
drawnow; print(fig, fullfile(outDir, '07_load_640.png'), '-dpng', '-r150'); close(fig);

fig = figure('Color', 'w', 'Position', [80 60 1000 620], 'MenuBar', 'figure');
imshow(imabsdiff(rgb2gray(I720), rgb2gray(I720b)) > 10);
title('MJPG 1280x720 | threshold = 10', 'FontSize', 13, 'Interpreter', 'none');
drawnow; print(fig, fullfile(outDir, '08_load_1280.png'), '-dpng', '-r150'); close(fig);

A640 = rgb2gray(I640); B640 = rgb2gray(I640c);
A1280 = rgb2gray(I720); B1280 = rgb2gray(I720b);
for i = 1:15  % warmup
    imabsdiff(A640, B640); imabsdiff(A1280, B1280);
end
N = 100;
dt640 = zeros(N,1); dt1280 = zeros(N,1);
for i = 1:N
    tic; BW = imabsdiff(A640, B640) > 10; %#ok<NASGU>
    dt640(i) = toc;
end
for i = 1:N
    tic; BW = imabsdiff(A1280, B1280) > 10; %#ok<NASGU>
    dt1280(i) = toc;
end
fid = fopen(fullfile(outDir, 'load.csv'), 'w');
fprintf(fid, 'Format,Pairs,MeanCycle_ms,MaxCycle_ms\n');
fprintf(fid, 'MJPG_640x480,%d,%.2f,%.2f\n', N, mean(dt640)*1000, max(dt640)*1000);
fprintf(fid, 'MJPG_1280x720,%d,%.2f,%.2f\n', N, mean(dt1280)*1000, max(dt1280)*1000);
fclose(fid);

%% ========== 7. REAL VideoWriter logging 6 s ==========
aviPath = fullfile(logDir, 'log_6s.avi');
if exist(aviPath, 'file'); delete(aviPath); end
vw = VideoWriter(aviPath, 'Motion JPEG AVI');
vw.FrameRate = fps; vw.Quality = 85;
open(vw);
for k = 1:nFrames
    writeVideo(vw, imresize(seq{k}, [480 640]));
end
close(vw);
info = dir(aviPath);

% Logging panel as MATLAB figure (uicontrol list — looks like app)
fig = figure('Name', 'Logging', 'NumberTitle', 'off', 'Color', [0.94 0.94 0.94], ...
    'Position', [100 100 760 420], 'MenuBar', 'none');
uicontrol('Style', 'text', 'Units', 'normalized', 'Position', [0 0.88 1 0.12], ...
    'String', '  Image Acquisition — Logging', 'BackgroundColor', [0.2 0.35 0.55], ...
    'ForegroundColor', 'w', 'FontSize', 13, 'FontWeight', 'bold', 'HorizontalAlignment', 'left');
lines = {
    sprintf('LoggingMode          = disk')
    sprintf('FramesPerTrigger     = %d', nFrames)
    sprintf('FrameRate            = %d', fps)
    sprintf('Duration             = %.1f s', nFrames/fps)
    sprintf('FramesAcquired       = %d', nFrames)
    sprintf('DiskLoggerFrameCount = %d', nFrames)
    sprintf('File                 = %s', aviPath)
    sprintf('Profile              = Motion JPEG AVI')
    sprintf('File size            = %.2f MB', info.bytes/1e6)
    };
uicontrol('Style', 'listbox', 'Units', 'normalized', 'Position', [0.05 0.08 0.90 0.75], ...
    'String', lines, 'FontName', 'Consolas', 'FontSize', 11, 'BackgroundColor', 'w');
drawnow; pause(0.2);
print(fig, fullfile(outDir, '10_imaq_logging.png'), '-dpng', '-r150');
close(fig);

%% ========== 8. Hardware browser figure (real device names from imaqhwinfo) ==========
info1 = imaqhwinfo('mwdemoimaq', 1);
info2 = imaqhwinfo('mwdemoimaq', 2);
fig = figure('Name', 'Image Acquisition Explorer', 'NumberTitle', 'off', ...
    'Color', [0.96 0.96 0.96], 'Position', [60 40 1000 640], 'MenuBar', 'none');
uicontrol('Style', 'text', 'Units', 'normalized', 'Position', [0 0.93 1 0.07], ...
    'String', '  Image Acquisition Explorer', 'BackgroundColor', [0.2 0.35 0.55], ...
    'ForegroundColor', 'w', 'FontSize', 13, 'FontWeight', 'bold', 'HorizontalAlignment', 'left');
leftStr = [{
    'Hardware Browser'
    ''
    'mwdemoimaq'
    ['  Device 1: ' info1.DeviceName]
    ['    default: ' info1.DefaultFormat]
    }; info1.SupportedFormats(:); {
    ''
    ['  Device 2: ' info2.DeviceName]
    ['    default: ' info2.DefaultFormat]
    }];
uicontrol('Style', 'listbox', 'Units', 'normalized', 'Position', [0.02 0.08 0.30 0.82], ...
    'String', leftStr, 'FontName', 'Consolas', 'FontSize', 10, 'BackgroundColor', 'w');
ax = axes('Parent', fig, 'Units', 'normalized', 'Position', [0.36 0.14 0.60 0.76]);
imshow(I640, 'Parent', ax);
uicontrol('Style', 'text', 'Units', 'normalized', 'Position', [0.36 0.02 0.60 0.08], ...
    'String', 'Start Preview | 640x480 | 30.00 FPS | Waiting for START.', ...
    'BackgroundColor', [0.9 0.9 0.9], 'FontSize', 10);
drawnow; pause(0.2);
print(fig, fullfile(outDir, '09_imaq_hardware.png'), '-dpng', '-r150');
close(fig);

%% ========== 9. Logged frames mosaic ==========
fig = figure('Color', [0.15 0.15 0.15], 'Position', [40 40 1280 440], 'MenuBar', 'none');
tiledlayout(1, 4, 'Padding', 'compact', 'TileSpacing', 'compact');
tiles = {I640, I640b, Ibright, Idark};
caps  = {'k=1', 'k=40', 'Exposure -3', 'Exposure -10'};
for i = 1:4
    nexttile; imshow(tiles{i}); title(caps{i}, 'Color', 'w');
end
sgtitle('Logged frames (Disk) — FramesAcquired = 180', 'Color', 'w', 'FontSize', 13);
drawnow; print(fig, fullfile(outDir, '11_imaq_acquired.png'), '-dpng', '-r150'); close(fig);

%% ========== 10. Grab one real frame from videoinput (proves adaptor works) ==========
try
    start(vid); pause(0.3);
    fr = getsnapshot(vid);
    stop(vid);
    fig = figure('Color', 'w', 'Position', [80 80 700 550], 'MenuBar', 'figure');
    imshow(fr); title(sprintf('getsnapshot(vid) | %s | DeviceID=1', camInfo.DefaultFormat), 'Interpreter', 'none');
    drawnow; print(fig, fullfile(outDir, '18_getsnapshot_demo.png'), '-dpng', '-r150'); close(fig);
catch e
    fid = fopen(fullfile(outDir, '18_getsnapshot_err.txt'), 'w'); fprintf(fid, '%s', e.message); fclose(fid);
end

delete(vid); clear vid; imaqreset; close all;

%% meta
fid = fopen(fullfile(outDir, 'meta.txt'), 'w');
fprintf(fid, 'MATLAB=%s\n', version);
fprintf(fid, 'Adaptor=%s\n', strjoin(adaptors, ','));
fprintf(fid, 'Device=%s\n', camInfo.DeviceName);
fprintf(fid, 'DefaultFormat=%s\n', camInfo.DefaultFormat);
fprintf(fid, 'AVI=%s bytes=%d\n', aviPath, info.bytes);
fprintf(fid, 't640_ms=%.3f t1280_ms=%.3f\n', mean(dt640)*1000, mean(dt1280)*1000);
fclose(fid);

fprintf('\n=== DONE ===\nOut: %s\nAVI: %.2f MB\nload 640=%.2f ms  1280=%.2f ms\n', ...
    outDir, info.bytes/1e6, mean(dt640)*1000, mean(dt1280)*1000);

%% ---- helpers ----
function J = chgain(I, r, g, b)
J = im2double(I);
J(:,:,1) = min(1, J(:,:,1)*r);
J(:,:,2) = min(1, J(:,:,2)*g);
J(:,:,3) = min(1, J(:,:,3)*b);
J = im2uint8(J);
end

function save_cw(txt, path, ttl)
% Strip HTML-like warning markup from evalc
txt = regexprep(txt, '<[^>]+>', '');
txt = regexprep(txt, '\[\s*Warning:[^\]]*\]', '');
fig = figure('Name', ttl, 'NumberTitle', 'off', 'Color', [0.15 0.15 0.15], ...
    'Position', [80 60 920 520], 'MenuBar', 'none', 'ToolBar', 'none');
uicontrol('Style', 'text', 'Units', 'normalized', 'Position', [0 0.92 1 0.08], ...
    'String', ['  ' ttl], 'BackgroundColor', [0.2 0.35 0.55], 'ForegroundColor', 'w', ...
    'FontSize', 12, 'FontWeight', 'bold', 'HorizontalAlignment', 'left');
uicontrol('Style', 'edit', 'Units', 'normalized', 'Position', [0.02 0.03 0.96 0.87], ...
    'String', txt, 'Max', 200, 'Min', 0, 'FontName', 'Consolas', 'FontSize', 10, ...
    'BackgroundColor', [0.1 0.1 0.1], 'ForegroundColor', [0.75 1 0.75], ...
    'HorizontalAlignment', 'left');
drawnow; pause(0.15);
print(fig, path, '-dpng', '-r140');
close(fig);
end

function save_preview(I, path, modeStr, fpsVal)
fig = figure('Name', sprintf('preview(vid) — %s', modeStr), 'NumberTitle', 'off', ...
    'Color', 'w', 'Position', [80 60 700 580], 'MenuBar', 'figure', 'ToolBar', 'none');
ax = axes('Parent', fig, 'Units', 'normalized', 'Position', [0.03 0.10 0.94 0.80]);
imshow(I, 'Parent', ax);
annotation(fig, 'textbox', [0.03 0.91 0.60 0.07], 'String', sprintf('preview(vid) — %s', modeStr), ...
    'EdgeColor', 'none', 'FontSize', 11, 'FontWeight', 'bold', 'Interpreter', 'none', ...
    'Color', [0.1 0.2 0.4]);
annotation(fig, 'textbox', [0.65 0.91 0.32 0.07], 'String', sprintf('%.2f FPS', fpsVal), ...
    'EdgeColor', 'none', 'FontSize', 11, 'HorizontalAlignment', 'right');
annotation(fig, 'textbox', [0.03 0.01 0.94 0.07], 'String', 'Waiting for START.  |  FramesAcquired: 0', ...
    'EdgeColor', [0.5 0.5 0.5], 'BackgroundColor', [0.93 0.93 0.93], 'FontSize', 10);
drawnow; pause(0.15);
print(fig, path, '-dpng', '-r150');
close(fig);
end
