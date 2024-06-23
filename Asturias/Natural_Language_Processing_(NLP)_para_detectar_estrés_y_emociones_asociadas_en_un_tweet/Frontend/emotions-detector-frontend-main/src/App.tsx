import './App.css';
import Result from './Result';
import SendText from './SendText';
import { Route, Routes, Link } from "react-router-dom"
function App() {

  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<SendText/>}/>
        <Route path="/result" element={<Result/>}/>
      </Routes>
    </div>
  );
}

export default App;
