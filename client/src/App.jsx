import './App.css';
import { Clock } from './components/Clock/Clock';
import { useState, useEffect } from 'react';
import { getClock } from './services/clockService';
import Loading from './components/Loading/Loading';

const nodeIPs = ["172.16.103.9:8088", "172.16.103.8:8088", "172.16.103.11:8088"];

function App() {
  const [clockData, setClockData] = useState({});
  const [errors, setErrors] = useState({});

  const fetchData = async () => {
    const results = await Promise.all(nodeIPs.map(ip => getClock(ip)));

    const data = {};
    const errs = {};

    results.forEach(result => {

      if (result.error) {
        errs[result.ip] = result.error;
      } else {
        data[result.ip] = result.data;
      }
    });

    setClockData(data);
    setErrors(errs);
  };

  useEffect(() => {
    fetchData();
    const id = setInterval(fetchData, 100); // Atualiza a cada 1 segundo

    return () => clearInterval(id);
  }, []);

  return (
    <>
      {nodeIPs.map((ip) => (
        clockData[ip] ? (
          <>
            <Clock
              key={`data-${ip}`}
              error={false}
              node={clockData[ip]?.node}
              time={clockData[ip]?.time}
              drift={clockData[ip]?.drift}
              leader={clockData[ip]?.leader}
              ip={ip}
            />
          </>

        ) : errors[ip] ? (
          <Clock
            key={`error-${ip}`}
            error={true}
            node={ip} // Exibe o IP no lugar do dado do nó
            time={errors[ip]} // Exibe a mensagem de erro
            ip={ip}
          />
        ) : (
          <Loading key={`loading-${ip}`}/>
        )
      ))}
    </>
  );
}

export default App;
