The libraries used are
1 - VLFeat
    To install VLFeat, download the binary package from
    https://www.vlfeat.org/download/vlfeat-0.9.21-bin.tar.gz
    and extract it to any directory of your choice. Let this be directory VLFEATROOT.

    Then, In MATLAB Command, run the following:
        run('VLFEATROOT\toolbox\vl_setup')
            For example, if I downloaded extracted the zip file into Program Files,
            the command would be
                run('C:/Program Files/vlfeat-0.9.21/toolbox/vl_setup')

    Then, to make sure that VLFeat is setup, run the following:
        vl_version verbose

        It should output something like:
            VLFeat version 0.9.17
            Static config: X64, little_endian, GNU C 40201 LP64, POSIX_threads, SSE2, OpenMP
            4 CPU(s): GenuineIntel MMX SSE SSE2 SSE3 SSE41 SSE42
            OpenMP: max threads: 4 (library: 4)
            Debug: yes
            SIMD enabled: yes

2 - Computer Vision Toolbox
    This can be easily downloaded using Add-Ons Explorer of MATLAB.
