import './App.css';
import { Input, Flex, Button, Typography, Slider } from 'antd';
import { useLocation } from 'react-router-dom';
import { useNavigate   } from "react-router-dom";

function Result() {

  interface Emotions {
    sadness: number;
    joy: number;
    love: number;
    anger: number;
    fear: number;
    surprise: number;
  }
  const navigate  = useNavigate();
  const {  Text, Title } = Typography;
  const { TextArea } = Input;

  const location = useLocation();
  const { state } = location;
  const { identifyingStress, ...data } = state;

  const emotions: Emotions = data || {
    sadness: 0,
    joy: 0,
    love: 0,
    anger: 0,
    fear: 0,
    surprise: 0,
  };
  console.log(identifyingStress) //{pred:"0"}

  // Convert the emotions object to an array of [key, value] pairs, and sort by value
  const sortedEmotions = Object.entries(emotions)
    .sort(([, valueA], [, valueB]) => valueB - valueA); // Sort in descending order[['sadness', 0.8799622654914856], ['fear', 0.07178837805986404]...]

  return (
      <Flex justify='center' align='center' style={{ minHeight: "100vh", backgroundColor: "#D3EBE5" }}>
        <Flex vertical justify="center" align='center' style={{ width: 500, minHeight: 550, borderRadius: 20, backgroundColor: "#E8D2EA", border: "4px solid #652B6B", }}>
          <Flex align='center'>
            <img style={{ widows: 70, height: 70, marginRight: 5 }} src='clouds.png'></img>
            <Title style={{ color: "#905596" }} level={3}>Your result</Title>
          </Flex>
          <Flex justify='center' align='center' style={{width:"80%", marginBottom:20}}>
            {identifyingStress.pred == 0 && 
              <>
                <Title style={{ color: "#2B6B5C" }} level={4}>You dont have stress</Title>
                <img style={{ width: 50, height: 50, marginLeft: 5 }} src={`stress0.png`} />
              </>
            }
            
            {identifyingStress.pred == 1 &&
              <>
                <Title style={{ color: "#2B6B5C" }} level={4}>You have stress</Title>
                <img style={{ width: 50, height: 50, marginLeft: 5 }} src={`stress1.png`} />
              </>
            }
            
          </Flex>
           {sortedEmotions.map(([emotion, value], index) => (
          <Flex vertical key={index} align='center' style={{ width: "80%", border: "1px solid #652B6B",borderRadius: 20,marginBottom:10 }}>
            <Flex style={{width:"60%"}} align="flex-start">
              <Text style={{color:"#2B6B5C"}}>
                You have   
                <Text style={{color:"#2B6B5C"}} strong> {parseFloat(value.toFixed(2))} </Text > 
                of 
                <Text style={{color:"#2B6B5C"}} strong> {emotion}</Text> 
              </Text>
            </Flex>
            <Flex justify='center' style={{ width: "100%" }}>
              <Slider
                min={0}
                max={1}
                step={0.01}
                value={value}
                style={{ width: "50%" }}
              />
              <img style={{ width: 30, height: 30, marginRight: 5 }} src={`${emotion}.png`} alt={emotion} />
            </Flex>
          </Flex>
        ))}
        <Button onClick={()=>{navigate("/")}} type="primary" style={{ backgroundColor: "#905596", marginBottom:30, marginTop:20 }}>Try again</Button>
        </Flex>
      </Flex>
  );
}

export default Result;
