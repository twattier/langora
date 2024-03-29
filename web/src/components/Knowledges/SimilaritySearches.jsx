import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'
import Divider from '@mui/material/Divider'
import CircularProgress from '@mui/material/CircularProgress'

import ListSimilaritySearches from '../Atoms/ListSimilaritySearches'
import { ContentBoxTitle } from '../../utils/style/component'
import { useFetchSimilarities } from '../../utils/hooks'

export default function SimilaritySearches(props) {
  const { query, onSelectSearch } = props

  const { similarities, isLoadingSimilarities, errorLoadingSimilarities } =
    useFetchSimilarities('searches', query)

  const handleSelectSearch = (search) => {
    if (onSelectSearch) {
      onSelectSearch(search)
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
          <ContentBoxTitle>Searches</ContentBoxTitle>
          <Divider />
          <ListSimilaritySearches
            searches={similarities.searches}
            onSelectSearch={handleSelectSearch}
          />
        </Stack>
      )}
    </Box>
  )
}
