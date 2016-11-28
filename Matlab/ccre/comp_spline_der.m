%   File: 'comp_spline_der.m'
%
%   Author(s):  Rogerio Richa
%   Created on: 2011
% 
%   (C) Copyright 2006-2011 Johns Hopkins University (JHU), All Rights
%   Reserved.
% 
% --- begin cisst license - do not edit ---
% 
% This software is provided "as is" under an open source license, with
% no warranty.  The complete license can be found in license.txt and
% http://www.cisst.org/cisst/license.txt.
% 
% --- end cisst license ---

function y = comp_spline_der(x)
y = zeros(1, numel(x));

y = and(x>=-2,x<-1).*( 3/2*(x+2).^2 ) + and(x>=-1, x<0).*( -4.5*x.^2-6.*x) + and(x>=0, x<1).*( 4.5*(x).^2-6*x) + and(x>=1, x<2).*( -3/2*(x-2).^2 );

y = y./3;