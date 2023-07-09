CS = crystalSymmetry('R3m', [8.0187, 8.0187, 10.1022],  'X||a', 'Z||c');

M = [[.00 .00 .00 .00 -0.46 -0.18]; [-0.18 0.18 .00 -0.46 .00 .00];[-0.31 -0.31 -0.67 .00 .00 .00]];

d = tensor(M, CS, 'rank',3,'propertyname','piezoelectric','unit','pC/N');

% figure

% plot3d(d.directionalMagnitude)

% ten = d.directionalMagnitude;

% surf(d.directionalMagnitude,'lower')
% x = Miller(1,0,0,'xyz',CS);
CS.properGroup

