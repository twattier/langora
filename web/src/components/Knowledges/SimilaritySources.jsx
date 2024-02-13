import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'
import Divider from '@mui/material/Divider'
import CircularProgress from '@mui/material/CircularProgress'

import ListSimilaritySources from '../Atoms/ListSimilaritySources'
import { ContentBoxTitle } from '../../utils/style/component'
import { useFetchSimilarities } from '../../utils/hooks'

export default function SimilaritySources(props) {
  const { query, onSelectSource } = props

  const { similarities, isLoadingSimilarities, errorLoadingSimilarities } =
    useFetchSimilarities('sources', query)

  const handleSelectSource = (source) => {
    if (onSelectSource) {
      onSelectSource(source)
    }
  }

  if (errorLoadingSimilarities) {
    return <span>Impossible to load similarity Sources</span>
  }

  return (
    <Box>
      {isLoadingSimilarities ? (
        <CircularProgress />
      ) : (
        <Stack spacing={1}>
          <ContentBoxTitle>Sources</ContentBoxTitle>
          <Divider />
          <ListSimilaritySources
            sources={similarities.sources}
            onSelectSource={handleSelectSource}
          />
        </Stack>
      )}
    </Box>
  )
}
