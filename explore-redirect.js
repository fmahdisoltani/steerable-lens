'use strict';
const destinations={'#results':'index.html#reconstruction-explorer','#trajectories':'imagenet.html#trajectories','#comparison':'index.html#comparison','#protocol':'index.html#measurements','#downloads':'index.html#resources'};
location.replace(destinations[location.hash] || 'index.html');
