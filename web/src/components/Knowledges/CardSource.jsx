import * as React from 'react'
import Box from '@mui/material/Box'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'
import Divider from '@mui/material/Divider'
import CircularProgress from '@mui/material/CircularProgress'
import Link from '@mui/material/Link'
import Accordion from '@mui/material/Accordion'
import AccordionSummary from '@mui/material/AccordionSummary'
import AccordionDetails from '@mui/material/AccordionDetails'
import ExpandMoreIcon from '@mui/icons-material/ExpandMore'

import { ContentBox, ContentBoxTitle } from '../../utils/style/component'
import SourceTexts from '../Atoms/SourceTexts'
import { DisplayLines } from '../../utils/display'
import { useFetchSource } from '../../utils/hooks'

export default function CardSource(props) {
  const { sourceId } = props

  const { source, isLoadingSource, errorLoadingSource } =
    useFetchSource(sourceId)
  if (errorLoadingSource) {
    return <span>Impossible to load the source</span>
  }

  const maxText = 175

  return (
    <ContentBox sx={{ width: '100%' }}>
      {isLoadingSource ? (
        <CircularProgress />
      ) : (
        <Stack spacing={1} sx={{ m: 1 }}>
          <ContentBoxTitle>{source.title}</ContentBoxTitle>
          <Divider />
          <Stack spacing={1}>
            <Box>
              <Typography variant="body1">{source.snippet}</Typography>
              <Link href={source.url} target="_blank" underline="none">
                <Typography variant="body2">{source.site}</Typography>
              </Link>
            </Box>

            <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }}>
              Extract
            </Typography>
            <Divider />
            {source?.extract === undefined ? (
              <Box>Scan Source</Box>
            ) : (
              <Accordion slotProps={{ transition: { unmountOnExit: true } }}>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography variant="body2" sx={{ mr: 2 }}>
                    {source.extract.length < maxText
                      ? source.extract
                      : source.extract.substr(0, maxText - 3) + '...'}
                  </Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <DisplayLines text={source.extract} variant="body2"/>
                </AccordionDetails>
              </Accordion>
            )}

            <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }}>
              Texts
            </Typography>
            <Divider />
            <SourceTexts sourceId={sourceId} sourceTexts={source.source_texts} />

            <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }}>
              Summary
            </Typography>
            <Divider />
            {source?.summary === null ? (
              <Box>Create Summary</Box>
            ) : (
              <Accordion slotProps={{ transition: { unmountOnExit: true } }}>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Typography variant="body2" sx={{ mr: 2 }}>
                    {source.summary.length < maxText
                      ? source.summary
                      : source.summary.substr(0, maxText - 3) + '...'}
                  </Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <DisplayLines text={source.summary} variant="body2" />
                </AccordionDetails>
              </Accordion>
            )}
          </Stack>
        </Stack>
      )}
    </ContentBox>
  )
}
