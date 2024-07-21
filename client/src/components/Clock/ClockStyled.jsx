import { styled } from "styled-components"

export const ClockContainer = styled.div`
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    width: 350px;
    border-radius: 10px;
    padding: 15px;
    margin: 5px;
    background-color: #25252D;
    color: #F1F1F4;
`

export const ClockNode = styled.span`
    font-size: 1.2rem;
    font-weight: 600;
    color: #B8B8C7;
`

export const ClockTimer = styled.div`
    font-size: 3rem;
    font-weight: 700;
`

export const ClockHour = styled.span``

export const ClockMinute = styled.span``

export const ClockSecond = styled.span``

export const Drift = styled.span`

`
