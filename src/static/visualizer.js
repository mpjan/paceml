document.addEventListener('DOMContentLoaded', () => {
  fetch('/workout')
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => {
      console.log('Received data:', data);
      renderWorkout(data);
    })
    .catch(error => {
      console.error('Error:', error);
      document.getElementById('error-message').textContent = `Error: ${error.message}`;
    });
});

function renderWorkout(workout) {
  console.log('Rendering workout:', workout);
  document.getElementById('workout-title').textContent = workout.metadata.title;
  document.getElementById('workout-info').textContent = 
    `${workout.metadata.date} - ${workout.metadata.athlete}`;

  const width = 800;
  const height = 400;
  const margin = { top: 20, right: 20, bottom: 30, left: 50 };

  const svg = d3.select('#visualization')
    .append('svg')
    .attr('width', width)
    .attr('height', height);

  const zoneColors = {
    'AR': '#91cf60',
    'RZ': '#1a9850',
    'MZ': '#fee08b',
    'TZ': '#fc8d59'
  };

  let y = 0;
  const intervals = workout.elements.flatMap(element => {
    if (element.type === 'interval') {
      return [element];
    } else if (element.type === 'repetition') {
      return Array(element.count).fill().flatMap(() => element.intervals);
    }
    return [];
  });

  const xScale = d3.scaleLinear()
    .domain([0, d3.sum(intervals, d => parseDuration(d.amount))])
    .range([margin.left, width - margin.right]);

  const yScale = d3.scaleBand()
    .domain(d3.range(intervals.length))
    .range([margin.top, height - margin.bottom])
    .padding(0.1);

  svg.selectAll('rect')
    .data(intervals)
    .enter()
    .append('rect')
    .attr('x', (d, i) => xScale(d3.sum(intervals.slice(0, i), int => parseDuration(int.amount))))
    .attr('y', (d, i) => yScale(i))
    .attr('width', d => xScale(parseDuration(d.amount)) - margin.left)
    .attr('height', yScale.bandwidth())
    .attr('fill', d => zoneColors[d.zone])
    .attr('class', 'interval');

  svg.selectAll('text')
    .data(intervals)
    .enter()
    .append('text')
    .attr('x', (d, i) => xScale(d3.sum(intervals.slice(0, i), int => parseDuration(int.amount))) + 5)
    .attr('y', (d, i) => yScale(i) + yScale.bandwidth() / 2)
    .attr('dy', '0.35em')
    .text(d => `${d.title} (${d.amount} - ${d.zone})`)
    .attr('class', 'interval-label');

  svg.append('g')
    .attr('transform', `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(xScale));
}

function parseDuration(amount) {
  if (amount.includes('km')) {
    return parseFloat(amount);
  } else if (amount.includes('min')) {
    return parseFloat(amount) / 60;
  } else if (amount.includes('s')) {
    return parseFloat(amount) / 3600;
  }
  return parseFloat(amount);
}