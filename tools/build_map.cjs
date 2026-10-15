// Generates assets/img/world-map.svg (Natural Earth 110m, public domain) with baked choropleth colours
const fs = require('fs'), path = require('path');
const topojson = require('topojson-client'), d3 = require('d3-geo');
const world = require('world-atlas/countries-110m.json');
const fc = topojson.feature(world, world.objects.countries);
fc.features = fc.features.filter(f => f.properties.name !== 'Antarctica' && f.properties.name !== 'Fr. S. Antarctic Lands');
const W = 640, H = 400;
const proj = d3.geoMercator().fitExtent([[2, 2], [W - 2, H - 2]], fc);
const p = d3.geoPath(proj); if (p.digits) p.digits(1);
const level = { 'United States of America': '#b90fd1', 'United Kingdom': '#c21fd8', 'Australia': '#e08af0', 'China': '#dc84ee', 'Canada': '#e7a9f2', 'France': '#ebb8f4', 'Germany': '#ebb8f4', 'Norway': '#eebff5' };
const paths = fc.features.map(f => { const d = p(f); if (!d) return ''; const n = f.properties.name; return `<path d="${d}" fill="${level[n] || '#f4d9f7'}"><title>${n.replace(/&/g,'&amp;')}</title></path>`; }).join('');
const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" role="img" aria-label="World map of visitors by country"><g stroke="#ffffff" stroke-width="0.6" stroke-linejoin="round">${paths}</g></svg>`;
fs.writeFileSync(path.join(__dirname, '../assets/img/world-map.svg'), svg);
console.log('map ok', (svg.length / 1024).toFixed(1) + 'KB');
