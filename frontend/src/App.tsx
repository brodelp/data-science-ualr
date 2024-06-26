import { useState } from 'react'
import ReactIframe from 'react-iframe'

const abbreviation_to_name = {
  "AK": "Alaska",
  "AL": "Alabama",
  "AR": "Arkansas",
  "AZ": "Arizona",
  "CA": "California",
  "CO": "Colorado",
  "CT": "Connecticut",
  "DE": "Delaware",
  "FL": "Florida",
  "GA": "Georgia",
  "HI": "Hawaii",
  "IA": "Iowa",
  "ID": "Idaho",
  "IL": "Illinois",
  "IN": "Indiana",
  "KS": "Kansas",
  "KY": "Kentucky",
  "LA": "Louisiana",
  "MA": "Massachusetts",
  "MD": "Maryland",
  "ME": "Maine",
  "MI": "Michigan",
  "MN": "Minnesota",
  "MO": "Missouri",
  "MS": "Mississippi",
  "MT": "Montana",
  "NC": "North Carolina",
  "ND": "North Dakota",
  "NE": "Nebraska",
  "NH": "New Hampshire",
  "NJ": "New Jersey",
  "NM": "New Mexico",
  "NV": "Nevada",
  "NY": "New York",
  "OH": "Ohio",
  "OK": "Oklahoma",
  "OR": "Oregon",
  "PA": "Pennsylvania",
  "RI": "Rhode Island",
  "SC": "South Carolina",
  "SD": "South Dakota",
  "TN": "Tennessee",
  "TX": "Texas",
  "UT": "Utah",
  "VA": "Virginia",
  "VT": "Vermont",
  "WA": "Washington",
  "WI": "Wisconsin",
  "WV": "West Virginia",
  "WY": "Wyoming",
}

function get_year_range() {
  const year = [];
  for (let i = 1950; i < 2017; i++) {
    year.push(i);
  }
  return year
}

function App() {
  
  const [mapType, setMapType] = useState('country')
  const [iframeURL, setIframeURL] = useState('/api/map/country/iframe')
  
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {


    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const year = formData.get('year')

    if (mapType == 'state') {
      const state = formData.get('state') as string
      const iframe_url = `/api/map/state/iframe?state=${state}&year=${year}`
      setIframeURL(iframe_url)
      console.log(iframe_url)

    } else if (mapType == 'country') {
      const iframe_url = `/api/map/country/iframe?&year=${year}`
      setIframeURL(iframe_url)
      console.log(iframe_url)
    }
  };

  // const handleGetMap = async () => {

  //   const iframe = await axios.get('/api/iframe')
    
  //   setIframeURL(flatData)
  // }

  return (
    <div className="h-full w-full">
      <div className="h-full w-full">
      <ReactIframe
          url={iframeURL}
          width="800px"
          height="600px"
          // Add controls for user interaction (optional)
          allow="fullscreen"
        />
        {/* <IframeView url={iframeURL}/> */}
      </div>
      <div>
        <select onChange={(e)=> setMapType(e.target.value)}>
          <option value='country'>Country Map</option>
          <option value='state'>State Map</option>
        </select>
        <FilterForm mapType={mapType} onSubmit={handleSubmit}/>
      </div>
    </div>
  )
}

// const IframeView = (props: {url: string}) => {
//   return (
//     <iframe 
//       src={props.url}
//       width='800'
//       height='600'>
//     </iframe>
//   )
// }

const FilterForm = (props: { mapType: string, onSubmit: React.FormEventHandler<HTMLFormElement> | undefined }) => {
  const years = get_year_range()

  if (props.mapType == 'state') {
    return (
      <form onSubmit={props.onSubmit}>
        <select name="state">
          {Object.entries(abbreviation_to_name).map(([key, value]) => 
              <option value={key}>{value}</option>
          )}
        </select>
        <select name="year">
          {years.map(year =>
            <option key={year} value={year}>{year}</option>
          )}
        </select>
        <button type="submit">Search</button>
      </form>
    )
  }
  else if (props.mapType == 'country') {
    return (
      <form onSubmit={props.onSubmit}>
        <select name="year">
          {years.map(year =>
            <option key={year} value={year}>{year}</option>
          )}
        </select>
        <button type="submit">Search</button>
      </form>
    )
  }
}

export default App
