import Box from '@mui/material/Box'
import Grid from '@mui/material/Grid'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import Divider from '@mui/material/Divider'
import CircularProgress from '@mui/material/CircularProgress'
import List from '@mui/material/List'
import ListItemButton from '@mui/material/ListItemButton'
import SearchIcon from '@mui/icons-material/Search'

import { ContentBoxTitle } from '../../utils/style/component'
import { useFetchSimilarities } from '../../utils/hooks'

export default function SimilaritySearches(props) {
  const { query, onSelectSearch } = props

  const { similarities, isLoadingSimilarities, errorLoadingSimilarities } =
    useFetchSimilarities('searches', query)

  const handleListItemClick = (event, item) => {
    if(onSelectSearch) {
      onSelectSearch(item)
    }
  }

  if (errorLoadingSimilarities) {
    return <span>Impossible to load similarity Searches</span>
  }

  return (
    <Box>
      {isLoadingSimilarities ? (
        <CircularProgress />
      ) : (
        <Stack spacing={1}>
          <ContentBoxTitle>Top Searches</ContentBoxTitle>
          <Divider />
          <List dense>
            {similarities.searches?.map((sim) => (
              <ListItemButton sx={{pt:0, pb:0}}
                onClick={(event) => handleListItemClick(event, sim.search)}
              >
                <Typography variant="body2" color="secondary" sx={{ mr: 2 }}>
                  {(sim.score_query * 100).toFixed(2)}%
                </Typography>
                <Typography variant="body2">
                  <SearchIcon sx={{ mr: 1 }} />
                  {`${sim.search.query} [${sim.search.nb_sources}]`}
                </Typography>
              </ListItemButton>
            ))}
          </List>          
        </Stack>
      )}
    </Box>
  )
}
