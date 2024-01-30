import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import Divider from '@mui/material/Divider'

import { ContentBox } from '../utils/style/component'
import ListItemSearch from './atoms/ListItemSearch'
import ListItemSource from './atoms/ListItemSource'

export default function GenAIResult(props) {
  const { resultGenAI } = props

  const DisplayLines = (props) => {
    const text = props.text;
    return text.split('\n').map(str => <p>{str}</p>);
  }

  return (
    <ContentBox>
      <DisplayLines text = {resultGenAI.response}/>
    </ContentBox>
  )
}
