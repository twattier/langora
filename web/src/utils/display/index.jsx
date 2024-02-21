import Typography from '@mui/material/Typography'

export const DisplayLines = (props) => {
    const {text, variant} = props
    return text.split('\n').map((str, index) => <Typography key={index} variant={variant}>{str}</Typography>)
  }
  