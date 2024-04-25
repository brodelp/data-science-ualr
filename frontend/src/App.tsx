import { useState } from 'react'
import axios from 'axios'

function App() {
  // const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
  //   event.preventDefault();
  //   const formData = new FormData(event.currentTarget);
  //   const id = formData.get('columnKey') as string
  //   const value = formData.get('columnVal') as string | number
  //   console.log(id)
  //   console.log(value)
    
  //   setColumnFilters({colKey: id, colVal: value});
  // };

  const [iframeURL, setIframeURL] = useState('/api/iframe')

  // const handleGetMap = async () => {

  //   const iframe = await axios.get('/api/iframe')
    
  //   setIframeURL(flatData)
  // }

  return (
    <div className="App">
      <h3>Iframes in React</h3>
      <iframe src={iframeURL}></iframe>
      {/* <button
        onClick={handleGetMap}
      >
      </button> */}
  </div>
  )
}

export default App
