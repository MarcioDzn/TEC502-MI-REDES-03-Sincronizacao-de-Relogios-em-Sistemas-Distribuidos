import { secondsToTime } from "../../utils/secondsToTime";
import { ClockContainer, ClockHour, ClockMinute, ClockSecond, ClockTimer, Drift, ClockNode } from "./ClockStyled";


export function Clock({error, node, time, leader, drift}) {
    const { hours, minutes, seconds: secs } = secondsToTime(time)
    return (
        <ClockContainer>
            <ClockNode>{node}</ClockNode>
            {
                error ? 
                <ClockTimer>
                    Indisponível
                </ClockTimer>
                :
                <ClockTimer>
                    <ClockHour>{hours}</ClockHour>
                    <span>:</span>
                    <ClockMinute>{minutes}</ClockMinute>
                    <span>:</span>
                    <ClockSecond>{secs}</ClockSecond>
                </ClockTimer>
            }
            {
                !error ? <Drift>Drift: {drift}</Drift> : <Drift>Drift: Nenhum</Drift>
            }

        </ClockContainer>
    )
}