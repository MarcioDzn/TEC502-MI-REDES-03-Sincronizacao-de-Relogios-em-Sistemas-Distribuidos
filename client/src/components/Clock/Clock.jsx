import { setDrift } from "../../services/clockService";
import { secondsToTime } from "../../utils/secondsToTime";
import { ClockContainer, ClockHour, ClockMinute, ClockSecond, ClockTimer, Drift, ClockNode } from "./ClockStyled";
import { useState, useEffect } from "react";

export function Clock({ error, node, time, leader, drift }) {
    const [isChangingDrift, setIsChangingDift] = useState(false);
    const [driftValue, setDriftValue] = useState("");

    const { hours, minutes, seconds: secs } = secondsToTime(time);

    const handleSubmit = (e) => {
        try{
            e.preventDefault();
            const floatDriftValue = parseFloat(driftValue);

            if (isNaN(floatDriftValue) || floatDriftValue < 0){
                throw new Error()
            }

            console.log(floatDriftValue)
            setDrift(node, floatDriftValue);
            setIsChangingDift(false); // Opcional: Fechar o formulário após a submissão
        } catch(err) {
            console.log("Erro")
        }

    };

    useEffect(() => {
        if (isChangingDrift) {
            const inputElement = document.querySelector('.drift');
            if (inputElement) {
                inputElement.focus();
                inputElement.select();
            }
        }
    }, [isChangingDrift]);

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
                !error ? !isChangingDrift ? 
                <Drift onClick={() => setIsChangingDift(true)}>Drift: {drift}</Drift> 
                : 
                <Drift>
                    Drift: 
                    <form onSubmit={handleSubmit}>
                        <input 
                            type="text" 
                            className={"drift"} 
                            value={driftValue} 
                            onChange={(e) => setDriftValue(e.target.value)} 
                        />
                    </form>  
                </Drift>
                
                : 
                <Drift>Drift: Nenhum</Drift>
            }
        </ClockContainer>
    );
}
