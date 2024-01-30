import Typography from '@mui/material/Typography'

export default function ListItemSearch(props) {
  const { search } = props
  return <Typography variant="body2">{search.query}</Typography>
}
