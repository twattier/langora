import List from '@mui/material/List'
import ListItemSource from './ListItemSource'

export default function ListSources(props) {
  const { sources } = props

  return (
    <List dense>
      {sources?.map((source) => (        
          <ListItemSource source={source} />
      ))}
    </List>
  )
}
