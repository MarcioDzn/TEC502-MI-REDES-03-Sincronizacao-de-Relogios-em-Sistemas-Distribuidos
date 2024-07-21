export function secondsToTime(seconds) {
    let hours = Math.floor(seconds / 3600);
    let minutes = Math.floor((seconds % 3600) / 60);
    let secs = seconds % 60;

    if (secs < 10) {
        secs = "0" + secs
    }

    if (minutes < 10) {
        minutes = "0" + minutes
    }

    if (hours < 10) {
        hours = "0" + hours
    }

    return { hours, minutes, seconds: secs };
  }