from .ATS import AlazarTech_ATS
from .utils import TraceParameter

from qcodes.utils import validators

class AlazarTech_ATS9360(AlazarTech_ATS):
    """
    This class is the driver for the ATS9360 board
    it inherits from the ATS base class

    TODO(nataliejpg):
        -  add clock source options and sample rate options
           (problem being that byte_to_value_dict of
           sample_rate relies on value of clock_source)

    """
    samples_divisor = 128

    def __init__(self, name, **kwargs):
        dll_path = 'C:\\WINDOWS\\System32\\ATSApi.dll'
        super().__init__(name, dll_path=dll_path, **kwargs)

        # add parameters

        # ----- Parameters for the configuration of the board -----
        self.add_parameter(name='clock_source',
                           parameter_class=TraceParameter,
                           get_cmd=None,
                           label='Clock Source',
                           unit=None,
                           initial_value='INTERNAL_CLOCK',
                           val_mapping={'INTERNAL_CLOCK': 1,
                                       'FAST_EXTERNAL_CLOCK': 2,
                                       'EXTERNAL_CLOCK_10MHz_REF': 7})
        self.add_parameter(name='external_sample_rate',
                           get_cmd=None,
                           parameter_class=TraceParameter,
                           label='External Sample Rate',
                           unit='S/s',
                           vals=validators.MultiType(validators.Ints(300000000, 1800000000),
                                                     validators.Enum('UNDEFINED')),
                           initial_value='UNDEFINED')
        self.add_parameter(name='sample_rate',
                           get_cmd=None,
                           parameter_class=TraceParameter,
                           label='Internal Sample Rate',
                           unit='S/s',
                           initial_value='UNDEFINED',
                           val_mapping={1_000: 1,
                                        2_000: 2,
                                        5_000: 4,
                                       10_000: 8,
                                       20_000: 10,
                                       50_000: 12,
                                      100_000: 14,
                                      200_000: 16,
                                      500_000: 18,
                                    1_000_000: 20,
                                    2_000_000: 24,
                                    5_000_000: 26,
                                   10_000_000: 28,
                                   20_000_000: 30,
                                   25_000_000: 33,
                                   50_000_000: 34,
                                  100_000_000: 36,
                                  125_000_000: 37,
                                  160_000_000: 38,
                                  180_000_000: 39,
                                  200_000_000: 40,
                                  250_000_000: 43,
                                  500_000_000: 48,
                                  800_000_000: 50,
                                1_000_000_000: 53,
                                1_200_000_000: 55,
                                1_500_000_000: 58,
                                1_800_000_000: 61,
                                2_000_000_000: 63,
                                2_400_000_000: 106,
                                3_000_000_000: 117,
                                3_600_000_000: 123,
                                4_000_000_000: 128,
                             'EXTERNAL_CLOCK': 64,
                                  'UNDEFINED': 'UNDEFINED'})
        self.add_parameter(name='clock_edge',
                           get_cmd=None,
                           parameter_class=TraceParameter,
                           label='Clock Edge',
                           unit=None,
                           initial_value='CLOCK_EDGE_RISING',
                           val_mapping={'CLOCK_EDGE_RISING': 0,
                                        'CLOCK_EDGE_FALLING': 1})
        self.add_parameter(name='decimation',
                           get_cmd=None,
                           parameter_class=TraceParameter,
                           label='Decimation',
                           unit=None,
                           initial_value=1,
                           vals=validators.Ints(0, 100000))

        for i in ['1', '2']:
            self.add_parameter(name='coupling' + i,
                               get_cmd=None,
                               parameter_class=TraceParameter,
                               label='Coupling channel ' + i,
                               unit=None,
                               initial_value='DC',
                               val_mapping={'AC': 1, 'DC': 2})
            self.add_parameter(name='channel_range' + i,
                               get_cmd=None,
                               parameter_class=TraceParameter,
                               label='Range channel ' + i,
                               unit='V',
                               initial_value=0.4,
                               val_mapping={0.4: 7})
            self.add_parameter(name='impedance' + i,
                               get_cmd=None,
                               parameter_class=TraceParameter,
                               label='Impedance channel ' + i,
                               unit='Ohm',
                               initial_value=50,
                               val_mapping={50: 2})

            self.add_parameter(name='bwlimit' + i,
                               get_cmd=None,
                               parameter_class=TraceParameter,
                               label='Bandwidth limit channel ' + i,
                               unit=None,
                               initial_value='DISABLED',
                               val_mapping={'DISABLED': 0,
                                            'ENABLED': 1})

        self.add_parameter(name='trigger_operation',
                           get_cmd=None,
                           parameter_class=TraceParameter,
                           label='Trigger Operation',
                           unit=None,
                           initial_value='TRIG_ENGINE_OP_J',
                           val_mapping={'TRIG_ENGINE_OP_J': 0,
                                        'TRIG_ENGINE_OP_K': 1,
                                        'TRIG_ENGINE_OP_J_OR_K': 2,
                                        'TRIG_ENGINE_OP_J_AND_K': 3,
                                        'TRIG_ENGINE_OP_J_XOR_K': 4,
                                        'TRIG_ENGINE_OP_J_AND_NOT_K': 5,
                                        'TRIG_ENGINE_OP_NOT_J_AND_K': 6})
        for i in ['1', '2']:
            self.add_parameter(name='trigger_engine' + i,
                               get_cmd=None,
                               parameter_class=TraceParameter,
                               label='Trigger Engine ' + i,
                               unit=None,
                               initial_value='TRIG_ENGINE_' + ('J' if i == '1' else 'K'),
                               val_mapping={'TRIG_ENGINE_J': 0,
                                            'TRIG_ENGINE_K': 1})
            self.add_parameter(name='trigger_source' + i,
                               get_cmd=None,
                               parameter_class=TraceParameter,
                               label='Trigger Source ' + i,
                               unit=None,
                               initial_value='EXTERNAL',
                               val_mapping={'CHANNEL_A': 0,
                                            'CHANNEL_B': 1,
                                            'EXTERNAL': 2,
                                            'DISABLE': 3})
            self.add_parameter(name='trigger_slope' + i,
                               get_cmd=None,
                               parameter_class=TraceParameter,
                               label='Trigger Slope ' + i,
                               unit=None,
                               initial_value='TRIG_SLOPE_POSITIVE',
                               val_mapping={'TRIG_SLOPE_POSITIVE': 1,
                                            'TRIG_SLOPE_NEGATIVE': 2})
            self.add_parameter(name='trigger_level' + i,
                               get_cmd=None,
                               parameter_class=TraceParameter,
                               label='Trigger Level ' + i,
                               unit=None,
                               initial_value=140,
                               vals=validators.Ints(0, 255))

        self.add_parameter(name='external_trigger_coupling',
                           get_cmd=None,
                           parameter_class=TraceParameter,
                           label='External Trigger Coupling',
                           unit=None,
                           initial_value='DC',
                           val_mapping={'AC': 1,'DC': 2})
        self.add_parameter(name='external_trigger_range',
                           get_cmd=None,
                           parameter_class=TraceParameter,
                           label='External Trigger Range',
                           unit=None,
                           initial_value='ETR_2V5',
                           val_mapping={'ETR_5V': 0, 'ETR_1V': 1,
                                        'ETR_TTL': 2, 'ETR_2V5': 3})
        self.add_parameter(name='trigger_delay',
                           get_cmd=None,
                           parameter_class=TraceParameter,
                           label='Trigger Delay',
                           unit='Sample clock cycles',
                           initial_value=0,
                           vals=validators.Multiples(divisor=8, min_value=0))
        # See Table 3 - Trigger Delay Alignment
        # TODO: this is either 8 or 16 dependent on the  number of channels in use

        # NOTE: The board will wait for a for this amount of time for a
        # trigger event.  If a trigger event does not arrive, then the
        # board will automatically trigger. Set the trigger timeout value
        # to 0 to force the board to wait forever for a trigger event.
        #
        # IMPORTANT: The trigger timeout value should be set to zero after
        # appropriate trigger parameters have been determined, otherwise
        # the board may trigger if the timeout interval expires before a
        # hardware trigger event arrives.
        self.add_parameter(name='timeout_ticks',
                           get_cmd=None,
                           parameter_class=TraceParameter,
                           label='Timeout Ticks',
                           unit='10 us',
                           initial_value=0,
                           vals=validators.Ints(min_value=0))

        self.add_parameter(name='aux_io_mode',
                           get_cmd=None,
                           parameter_class=TraceParameter,
                           label='AUX I/O Mode',
                           unit=None,
                           initial_value='AUX_IN_AUXILIARY',
                           val_mapping={'AUX_OUT_TRIGGER': 0,
                                        'AUX_IN_TRIGGER_ENABLE': 1,
                                        'AUX_IN_AUXILIARY': 13})
        self.add_parameter(name='aux_io_param',
                           get_cmd=None,
                           parameter_class=TraceParameter,
                           label='AUX I/O Param',
                           unit=None,
                           initial_value='NONE',
                           val_mapping={'NONE': 0,
                                        'TRIG_SLOPE_POSITIVE': 1,
                                        'TRIG_SLOPE_NEGATIVE': 2})

        # ----- Parameters for the acquire function -----
        self.add_parameter(name='mode',
                           label='Acquisition mode',
                           unit=None,
                           initial_value='NPT',
                           get_cmd=None,
                           set_cmd=None,
                           val_mapping={'NPT': 0x200, 'TS': 0x400})
        self.add_parameter(name='samples_per_record',
                           label='Samples per Record',
                           unit=None,
                           initial_value=1024,
                           get_cmd=None,
                           set_cmd=None,
                           vals=validators.Multiples(
                                divisor=self.samples_divisor, min_value=256))
        self.add_parameter(name='records_per_buffer',
                           label='Records per Buffer',
                           unit=None,
                           initial_value=10,
                           get_cmd=None,
                           set_cmd=None,
                           vals=validators.Ints(min_value=0))
        self.add_parameter(name='buffers_per_acquisition',
                           label='Buffers per Acquisition',
                           unit=None,
                           get_cmd=None,
                           set_cmd=None,
                           initial_value=10,
                           vals=validators.Ints(min_value=0))
        self.add_parameter(name='channel_selection',
                           label='Channel Selection',
                           unit=None,
                           get_cmd=None,
                           set_cmd=None,
                           initial_value='AB',
                           val_mapping={'A': 1, 'B': 2, 'AB': 3})
        self.add_parameter(name='transfer_offset',
                           label='Transfer Offset',
                           unit='Samples',
                           get_cmd=None,
                           set_cmd=None,
                           initial_value=0,
                           vals=validators.Ints(min_value=0))
        self.add_parameter(name='external_startcapture',
                           label='External Startcapture',
                           unit=None,
                           get_cmd=None,
                           set_cmd=None,
                           initial_value='ENABLED',
                           val_mapping={'DISABLED': 0X0,
                                        'ENABLED': 0x1})
        self.add_parameter(name='enable_record_headers',
                           label='Enable Record Headers',
                           unit=None,
                           get_cmd=None,
                           set_cmd=None,
                           initial_value='DISABLED',
                           val_mapping={'DISABLED': 0x0,
                                        'ENABLED': 0x8})
        self.add_parameter(name='alloc_buffers',
                           label='Alloc Buffers',
                           unit=None,
                           get_cmd=None,
                           set_cmd=None,
                           initial_value='DISABLED',
                           val_mapping={'DISABLED': 0x0,
                                        'ENABLED': 0x20})
        self.add_parameter(name='fifo_only_streaming',
                           label='Fifo Only Streaming',
                           unit=None,
                           get_cmd=None,
                           set_cmd=None,
                           initial_value='DISABLED',
                           val_mapping={'DISABLED': 0x0,
                                        'ENABLED': 0x800})
        self.add_parameter(name='interleave_samples',
                           label='Interleave Samples',
                           unit=None,
                           get_cmd=None,
                           set_cmd=None,
                           initial_value='DISABLED',
                           val_mapping={'DISABLED': 0x0,
                                        'ENABLED': 0x1000})
        self.add_parameter(name='get_processed_data',
                           label='Get Processed Data',
                           unit=None,
                           get_cmd=None,
                           set_cmd=None,
                           initial_value='DISABLED',
                           val_mapping={'DISABLED': 0x0,
                                        'ENABLED': 0x2000})
        self.add_parameter(name='allocated_buffers',
                           label='Allocated Buffers',
                           unit=None,
                           get_cmd=None,
                           set_cmd=None,
                           initial_value=4,
                           vals=validators.Ints(min_value=0))
        self.add_parameter(name='buffer_timeout',
                           label='Buffer Timeout',
                           unit='ms',
                           get_cmd=None,
                           set_cmd=None,
                           initial_value=1000,
                           vals=validators.Ints(min_value=0))

        model = self.get_idn()['model']
        if model != 'ATS9360':
            raise Exception("The Alazar board kind is not 'ATS9360',"
                            " found '" + str(model) + "' instead.")
