function formatDate(date) {
  const day = date.toLocaleString('en-US', { weekday: 'long' });
  const month = date.toLocaleString('en-US', { month: 'long' });
  const dayNumber = date.getDate();
  const year = date.getFullYear();
  return `${day} ${dayNumber}${getDaySuffix(dayNumber)} ${month} ${year}`;
}

function getDaySuffix(day) {
  if (day >= 11 && day <= 13) {
    return 'th';
  }
  const lastDigit = day % 10;
  switch (lastDigit) {
    case 1: return 'st';
    case 2: return 'nd';
    case 3: return 'rd';
    default: return 'th';
  }
}

function updateDisplayedDate(startDate, endDate) {
  const selectedDateElement = document.getElementById('selected-date');
  selectedDateElement.textContent = `${formatDate(startDate)} - ${formatDate(endDate)}`;
}

function getStartOfCurrentWeek(date) {
  const dayOfWeek = date.getDay();
  const diff = date.getDate() - dayOfWeek + (dayOfWeek === 0 ? -6 : 1); // Adjust for Sunday
  return new Date(date.getFullYear(), date.getMonth(), diff);
}

function getEndOfCurrentWeek(startDate) {
  const endDate = new Date(startDate);
  endDate.setDate(startDate.getDate() + 6);
  return endDate;
}

function changeWeek(weekOffset) {
  const selectedDateElement = document.getElementById('selected-date');
  const currentDate = new Date(selectedDateElement.textContent.split(' ')[1]);
  currentDate.setDate(currentDate.getDate() + (7 * weekOffset));
  const startOfWeek = getStartOfCurrentWeek(currentDate);
  const endOfWeek = getEndOfCurrentWeek(startOfWeek);
  updateDisplayedDate(startOfWeek, endOfWeek);
}

window.onload = function () {
  const currentDate = new Date();
  const startOfCurrentWeek = getStartOfCurrentWeek(currentDate);
  const endOfCurrentWeek = getEndOfCurrentWeek(startOfCurrentWeek);
  updateDisplayedDate(startOfCurrentWeek, endOfCurrentWeek);
};