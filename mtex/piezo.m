CS = crystalSymmetry('R3m', [8.0187, 8.0187, 10.1022], [90.0000, 90.000, 120.0000]*degree, 'X||a', 'Z||c');

M = [[.00 .00 .00 .00 -0.46 -0.18]; [-0.18 0.18 .00 -0.46 .00 .00];[-0.31 -0.31 -0.67 .00 .00 .00]];

d = tensor(M, CS, 'rank',3,'propertyname','piezoelectric','unit','pC/N');

% plot(d,'complete','smooth','upper');
% plot(Cs,'3d')


plot(d,'3d','complete','smooth','upper')
% (d.directionalMagnitude,'upper')

mtexColorbar

rotate3d