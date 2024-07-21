import { createGlobalStyle } from "styled-components"

export const GlobalStyle = createGlobalStyle`
    *{
        padding: 0;
        margin: 0;
        font-family: "Montserrat", sans-serif;
        font-optical-sizing: auto;
        font-style: : normal;
        box-sizing: border-box;
    }

    html, body {
        height: 100%;
    }

    #root {
        height: 90.6vh;
    }
` 