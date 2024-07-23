import { secondsToTime } from "../../utils/secondsToTime";
import { ClockContainer, EditClock, ClockHour, ClockMinute, ClockSecond, ClockTimer, Drift, ClockNode } from "./ClockStyled";
import {useState} from "react"


export function Clock({error, node, time, leader, drift}) {
    const [isChangingDrift, setIsChangingDift] = useState(false)
    const { hours, minutes, seconds: secs } = secondsToTime(time)
    console.log(node + leader)
    return (
        <ClockContainer is_leader={leader}>
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
                
            !error ? !isChangingDrift ? <Drift onClick={() => {isChangingDrift ? setIsChangingDift(false) : setIsChangingDift(true)}}>Drift: {drift}</Drift> : 
                <form onSubmit={() => {

                }}>
                    <input type="text"/>
                    <button type="submit">a</button>
                </form>  : 
                <Drift>Drift: Nenhum</Drift>
                
                
    
            }

        </ClockContainer>
    )
}