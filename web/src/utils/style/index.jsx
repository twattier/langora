import { createTheme } from '@mui/material/styles'

export const layout = {
  bannerHeight: 100,
}

export const colors = {
  txtBanner: '#fff',
}

export const theme = createTheme({
  palette: {
    primary: {      
      main: '#1b5875',
      dark: '#003147',
      light: '#578faf'
    },
  },
  
  typography: {
    h5: {
      fontWeight: 500,
      fontSize: 26,
      letterSpacing: 0.5,
    },
  },
  shape: {
    borderRadius: 8,
  },
  components: {
    MuiDrawer: {
      styleOverrides: {
        paper: {
          backgroundColor: '#081627',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
        },
        contained: {
          boxShadow: 'none',
          '&:active': {
            boxShadow: 'none',
          },
        },
      },
    },
    MuiTabs: {
      styleOverrides: {
        root: {
          marginLeft: 1,
        },
        indicator: {
          height: 3,
          borderTopLeftRadius: 3,
          borderTopRightRadius: 3,
          backgroundColor: '#000',
        },
      },
    },
    MuiTab: {
      defaultProps: {
        disableRipple: true,
      },
      styleOverrides: {
        root: {
          textTransform: 'none',
          margin: '0 16px',
          minWidth: 0,
          padding: 0,
          // [theme.breakpoints.up('md')]: {
          //   padding: 0,
          //   minWidth: 0,
          // },
        },
      },
    },
    MuiIconButton: {
      styleOverrides: {
        root: {
          padding: 1,
        },
      },
    },
    MuiTooltip: {
      styleOverrides: {
        tooltip: {
          borderRadius: 4,
        },
      },
    },
    MuiDivider: {
      styleOverrides: {
        root: {
          backgroundColor: 'rgb(255,255,255,0.15)',
        },
      },
    },
    MuiListItemButton: {
      styleOverrides: {
        root: {
          '&.Mui-selected': {
            color: '#4fc3f7',
          },
        },
      },
    },
    MuiListItemText: {
      styleOverrides: {        
        primary: {
          marginLeft: 10,
          fontSize: 14,
          fontWeight: 'bolder',
        },
      },
    },
    MuiListItemIcon: {
      styleOverrides: {
        root: {
          color: 'inherit',
          minWidth: 'auto',
          marginRight: 1,
          '& svg': {
            fontSize: 20,
          },
        },
      },
    },
    MuiAvatar: {
      styleOverrides: {
        root: {
          width: 32,
          height: 32,
        },
      },
    },
    MuiGridItem: {
      styleOverrides: {
        root: {
          paddingLeft: 0,
          paddingTop: 0,
        },
      },
    },
  },
  mixins: {
    toolbar: {
      minHeight: 48,
    },
  },
})
