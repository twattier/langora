import Typography from '@mui/material/Typography'

export const DisplayLines = (props) => {
    const text = props.text
    return text.split('\n').map((str) => <Typography>{str}</Typography>)
  }