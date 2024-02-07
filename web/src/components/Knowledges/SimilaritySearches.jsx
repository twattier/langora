import Box from '@mui/material/Box'
import Grid from '@mui/material/Grid'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import Divider from '@mui/material/Divider'
import CircularProgress from '@mui/material/CircularProgress'

import ListItemSearch from '../atoms/ListItemSearch'
import { useFetchSimilarities } from '../../utils/hooks'

export default function SimilaritySearches(props) {
  const { query } = props

  const { similarities, isLoadingSimilarities, errorLoadingSimilarities } =
    useFetchSimilarities('searches', query)
  if (errorLoadingSimilarities) {
    return <span>Impossible to load similarity Searches</span>
  }

  return (
    <Box>
      {isLoadingSimilarities ? (
        <CircularProgress />
      ) : (
        <Stack spacing={1}>
          <Typography variant="subtitle2" sx={{ fontWeight: 'bold' }}>
            Searches
          </Typography>
          <Divider />
          <Box sw={{ width: '100%' }}>
            {similarities.searches?.map((sim) => (
              <ListItemSearch search={sim.search} />
            ))}
          </Box>
        </Stack>
      )}
    </Box>
  )
}
