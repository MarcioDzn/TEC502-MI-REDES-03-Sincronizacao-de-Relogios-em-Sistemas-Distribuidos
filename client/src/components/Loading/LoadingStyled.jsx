import { styled, keyframes } from "styled-components"

// Definir a animação de rotação
const spin = keyframes`
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
`;

// Criar o componente de círculo giratório
export const Spinner = styled.div`
  border: ${(props) => props.size == "normal" ? `8px` : `3px`} solid #f3f3f3; /* Cor de fundo */
  border-top: ${(props) => props.size == "normal" ? `8px` : `3px`} solid #25252D;; /* Cor do círculo giratório */
  border-radius: 50%;
  width: ${(props) => props.size == "normal" ? `35px` : `20px`};
  height: ${(props) => props.size == "normal" ? `35px` : `20px`};
  animation: ${spin} 1s linear infinite;
  margin: ${(props) => props.size == "normal" ? `auto` : `none`};
`;



