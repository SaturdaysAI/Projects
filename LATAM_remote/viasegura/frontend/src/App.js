import './App.css';
import Cabecera from './components/Cabecera'
import Mapa from './components/Mapa';
import Tabla from './components/Tabla';

function App() {
  return (
    <div className="App">
      <Cabecera />
      <div className='container-fluid' >
        <div className="row row-cols-2" style={{height: '80vh'}}>
          <div className="col-4 p-3">Column</div>
          <div className="col-8 p-3 "><Mapa/></div>
          <div className="col-4 p-3">Column</div>
          <div className="col-8 p-3 "><Tabla/></div>
        </div>
      </div>
    </div>
  );
}

export default App;
