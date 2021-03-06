{
  'variables': {
    'arch%': 'amd64', # linux JVM architecture. See $(JAVA_HOME)/jre/lib/<@(arch)/server/
    'conditions': [
      ['target_arch=="ia32"', {
        'arch%': 'i386'
      }],
      ['OS=="win"', {
        'javahome%': '<!(node findJavaHome.js)'
      }],
      ['OS=="linux" or OS=="mac" or OS=="freebsd" or OS=="openbsd"', {
        'javahome%': '<!(node findJavaHome.js)'
      }],
      ['OS=="mac"', {
      	'javaver%' : "<!(awk -F/ -v h=`node findJavaHome.js` 'BEGIN {n=split(h, a); print a[2]; exit}')"
      }]
    ]
  },
  'targets': [
    {
      'target_name': 'nodejavabridge_bindings',
      'sources': [
        'src/java.cpp',
        'src/javaObject.cpp',
        'src/javaScope.cpp',
        'src/methodCallBaton.cpp',
        'src/nodeJavaBridge.cpp',
        'src/utils.cpp'
      ],
      'include_dirs': [
        '<(javahome)/include',
      ],
      'cflags': ['-O3'],
      'conditions': [
        ['OS=="win"',
          {
            'actions': [
              {
                'action_name': 'verifyDeps',
                'inputs': [
                  '<(javahome)/lib/jvm.lib',
                  '<(javahome)/include/jni.h',
                  '<(javahome)/include/win32/jni_md.h'
                ],
                'outputs': ['./build/depsVerified'],
                'action': ['python', 'touch.py'],
                'message': 'Verify Deps'
              }
            ],
            'include_dirs': [
              '<(javahome)/include/win32',
            ],
            'libraries': [
              '-l<(javahome)/lib/jvm.lib'
            ]
          }
        ],
        ['OS=="linux"',
          {
            'actions': [
              {
                'action_name': 'verifyDeps',
                'inputs': [
                  '<(javahome)/jre/lib/<(arch)/server/libjvm.so',
                  '<(javahome)/include/jni.h',
                  '<(javahome)/include/linux/jni_md.h'
                ],
                'outputs': ['./build/depsVerified'],
                'action': [],
                'message': 'Verify Deps'
              }
            ],
            'include_dirs': [
              '<(javahome)/include/linux',
            ],
            'libraries': [
              '-L<(javahome)/jre/lib/<(arch)/server/',
              '-Wl,-rpath,<(javahome)/jre/lib/<(arch)/server/',
              '-ljvm'
            ]
          }
        ],
        ['OS=="freebsd"',
          {
            'actions': [
              {
                'action_name': 'verifyDeps',
                'inputs': [
                  '<(javahome)/jre/lib/<(arch)/server/libjvm.so',
                  '<(javahome)/include/jni.h',
                  '<(javahome)/include/freebsd/jni_md.h'
                ],
                'outputs': ['./build/depsVerified'],
                'action': [],
                'message': 'Verify Deps'
              }
            ],
            'include_dirs': [
              '<(javahome)/include/freebsd',
            ],
            'libraries': [
              '-L<(javahome)/jre/lib/<(arch)/server/',
              '-Wl,-rpath,<(javahome)/jre/lib/<(arch)/server/',
              '-ljvm'
            ]
          }
        ],
        ['OS=="openbsd"',
          {
            'actions': [
              {
                'action_name': 'verifyDeps',
                'inputs': [
                  '<(javahome)/jre/lib/<(arch)/server/libjvm.so',
                  '<(javahome)/include/jni.h',
                  '<(javahome)/include/openbsd/jni_md.h'
                ],
                'outputs': ['./build/depsVerified'],
                'action': [],
                'message': 'Verify Deps'
              }
            ],
            'include_dirs': [
              '<(javahome)/include/openbsd',
            ],
            'libraries': [
              '-L<(javahome)/jre/lib/<(arch)/server/',
              '-Wl,-rpath,<(javahome)/jre/lib/<(arch)/server/',
              '-ljvm'
            ]
          }
        ],
        ['OS=="mac"',
          {
            'xcode_settings': {
              'OTHER_CFLAGS': ['-O3'],
            },
            'conditions': [
              ['javaver=="Library"',
                {
                  'include_dirs': [
                    '<(javahome)/include',
                    '<(javahome)/include/darwin'
                  ],
                  'libraries': [
                    '-L<(javahome)/jre/lib/server',
                    '-Wl,-rpath,<(javahome)/jre/lib/server',
                    '-ljvm'
                  ],
                },
              ],
              ['javaver=="System"',
                {
                  'include_dirs': [
                    '/System/Library/Frameworks/JavaVM.framework/Headers'
                  ],
                  'libraries': [
                    '-framework JavaVM'
                  ],
                },
              ],
              ['javaver==""',
                {
                  'include_dirs': [
                    '/System/Library/Frameworks/JavaVM.framework/Headers'
                  ],
                  'libraries': [
                    '-framework JavaVM'
                  ],
                },
              ],
            ],
          },
        ],
      ]
    }
  ]
}
