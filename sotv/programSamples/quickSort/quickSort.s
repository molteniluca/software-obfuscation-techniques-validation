	.file	"quickSort.c"
	.section	.rodata.str1.1,"aMS",@progbits,1
.LC0:
	.string	"\n ["
.LC1:
	.string	"%d, "
.LC2:
	.string	"%d]"
	.section	.text.unlikely,"ax",@progbits
.LCOLDB3:
	.text
.LHOTB3:
	.p2align 4,,15
	.globl	print_array
	.type	print_array, @function
print_array:
.LFB38:
	.cfi_startproc
	pushq	%r12
	.cfi_def_cfa_offset 16
	.cfi_offset 12, -16
	movq	%rdi, %r12
	pushq	%rbp
	.cfi_def_cfa_offset 24
	.cfi_offset 6, -24
	leaq	396(%r12), %rbp
	pushq	%rbx
	.cfi_def_cfa_offset 32
	.cfi_offset 3, -32
	movl	$.LC0, %esi
	movl	$1, %edi
	xorl	%eax, %eax
	movq	%r12, %rbx
	call	__printf_chk
	.p2align 4,,10
	.p2align 3
.L2:
	movl	(%rbx), %edx
	xorl	%eax, %eax
	movl	$.LC1, %esi
	movl	$1, %edi
	addq	$4, %rbx
	call	__printf_chk
	cmpq	%rbp, %rbx
	jne	.L2
	popq	%rbx
	.cfi_def_cfa_offset 24
	movl	396(%r12), %edx
	movl	$.LC2, %esi
	movl	$1, %edi
	popq	%rbp
	.cfi_def_cfa_offset 16
	popq	%r12
	.cfi_def_cfa_offset 8
	xorl	%eax, %eax
	jmp	__printf_chk
	.cfi_endproc
.LFE38:
	.size	print_array, .-print_array
	.section	.text.unlikely
.LCOLDE3:
	.text
.LHOTE3:
	.section	.text.unlikely
.LCOLDB4:
	.text
.LHOTB4:
	.p2align 4,,15
	.globl	swap
	.type	swap, @function
swap:
.LFB39:
	.cfi_startproc
	movl	(%rdi), %eax
	movl	(%rsi), %edx
	movl	%edx, (%rdi)
	movl	%eax, (%rsi)
	ret
	.cfi_endproc
.LFE39:
	.size	swap, .-swap
	.section	.text.unlikely
.LCOLDE4:
	.text
.LHOTE4:
	.section	.text.unlikely
.LCOLDB5:
	.text
.LHOTB5:
	.p2align 4,,15
	.globl	quicksort
	.type	quicksort, @function
quicksort:
.LFB40:
	.cfi_startproc
	pushq	%r15
	.cfi_def_cfa_offset 16
	.cfi_offset 15, -16
	pushq	%r14
	.cfi_def_cfa_offset 24
	.cfi_offset 14, -24
	movq	%rdi, %r9
	pushq	%r13
	.cfi_def_cfa_offset 32
	.cfi_offset 13, -32
	pushq	%r12
	.cfi_def_cfa_offset 40
	.cfi_offset 12, -40
	movl	%esi, %r15d
	pushq	%rbp
	.cfi_def_cfa_offset 48
	.cfi_offset 6, -48
	pushq	%rbx
	.cfi_def_cfa_offset 56
	.cfi_offset 3, -56
	movl	%edx, %ebx
	subq	$72, %rsp
	.cfi_def_cfa_offset 128
	movl	%edx, 52(%rsp)
.L15:
	movslq	%r15d, %r11
	movl	%ebx, %eax
	movl	(%r9,%r11,4), %esi
	movl	%r11d, %ecx
.L8:
	cmpl	%eax, %ecx
	jg	.L12
	movslq	%ecx, %rdx
	salq	$2, %rdx
	leaq	(%r9,%rdx), %r10
	movl	(%r10), %ebx
	cmpl	%ebx, %esi
	jle	.L13
	leaq	4(%r9,%rdx), %rdx
.L9:
	movq	%rdx, %r10
	leaq	4(%rdx), %rdx
	movl	-4(%rdx), %ebx
	addl	$1, %ecx
	cmpl	%ebx, %esi
	jg	.L9
	movslq	%eax, %rdx
	salq	$2, %rdx
	leaq	(%r9,%rdx), %r8
	movl	(%r8), %edi
	cmpl	%esi, %edi
	jle	.L157
.L98:
	leaq	-4(%r9,%rdx), %rdx
.L11:
	movq	%rdx, %r8
	leaq	-4(%rdx), %rdx
	movl	4(%rdx), %edi
	subl	$1, %eax
	cmpl	%edi, %esi
	jl	.L11
.L157:
	cmpl	%ecx, %eax
	jge	.L89
.L12:
	cmpl	%eax, %r15d
	movl	%ecx, 28(%rsp)
	movl	%eax, 32(%rsp)
	jl	.L24
.L25:
	movl	28(%rsp), %esi
	cmpl	%esi, 52(%rsp)
	jle	.L162
	movl	%esi, %r15d
	movl	52(%rsp), %ebx
	jmp	.L15
.L13:
	movslq	%eax, %rdx
	salq	$2, %rdx
	leaq	(%r9,%rdx), %r8
	movl	(%r8), %edi
	cmpl	%edi, %esi
	jl	.L98
.L89:
	movl	%edi, (%r10)
	addl	$1, %ecx
	movl	%ebx, (%r8)
	subl	$1, %eax
	jmp	.L8
.L162:
	addq	$72, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 56
	popq	%rbx
	.cfi_def_cfa_offset 48
	popq	%rbp
	.cfi_def_cfa_offset 40
	popq	%r12
	.cfi_def_cfa_offset 32
	popq	%r13
	.cfi_def_cfa_offset 24
	popq	%r14
	.cfi_def_cfa_offset 16
	popq	%r15
	.cfi_def_cfa_offset 8
	ret
.L163:
	.cfi_restore_state
	movslq	%eax, %rdx
	salq	$2, %rdx
	leaq	(%r9,%rdx), %rdi
	movl	(%rdi), %r8d
	cmpl	%r8d, %esi
	jge	.L19
.L99:
	leaq	-4(%r9,%rdx), %rdx
.L20:
	movq	%rdx, %rdi
	leaq	-4(%rdx), %rdx
	movl	4(%rdx), %r8d
	subl	$1, %eax
	cmpl	%r8d, %esi
	jl	.L20
	cmpl	%ecx, %eax
	jge	.L90
.L21:
	cmpl	%eax, %r15d
	movl	%ecx, 36(%rsp)
	movl	%eax, 40(%rsp)
	jl	.L33
.L34:
	movl	36(%rsp), %esi
	cmpl	%esi, 32(%rsp)
	jle	.L25
	movl	32(%rsp), %eax
	movslq	%esi, %r11
	movl	%r11d, %r15d
.L24:
	movl	(%r9,%r11,4), %esi
	movl	%r15d, %ecx
.L17:
	cmpl	%eax, %ecx
	jg	.L21
	movslq	%ecx, %rdx
	salq	$2, %rdx
	leaq	(%r9,%rdx), %r10
	movl	(%r10), %ebx
	cmpl	%ebx, %esi
	jle	.L22
	leaq	4(%r9,%rdx), %rdx
.L18:
	movq	%rdx, %r10
	leaq	4(%rdx), %rdx
	movl	-4(%rdx), %ebx
	addl	$1, %ecx
	cmpl	%ebx, %esi
	jg	.L18
	jmp	.L163
.L22:
	movslq	%eax, %rdx
	salq	$2, %rdx
	leaq	(%r9,%rdx), %rdi
	movl	(%rdi), %r8d
	cmpl	%r8d, %esi
	jl	.L99
.L90:
	movl	%r8d, (%r10)
	addl	$1, %ecx
	movl	%ebx, (%rdi)
	subl	$1, %eax
	jmp	.L17
	.p2align 4,,10
	.p2align 3
.L164:
	movslq	%eax, %rdx
	salq	$2, %rdx
	leaq	(%r9,%rdx), %rdi
	movl	(%rdi), %r8d
	cmpl	%r8d, %esi
	jge	.L28
.L100:
	leaq	-4(%r9,%rdx), %rdx
.L29:
	movq	%rdx, %rdi
	leaq	-4(%rdx), %rdx
	movl	4(%rdx), %r8d
	subl	$1, %eax
	cmpl	%r8d, %esi
	jl	.L29
	cmpl	%ecx, %eax
	jge	.L91
.L138:
	movl	%eax, %esi
	movl	%ecx, 20(%rsp)
	movl	%eax, 12(%rsp)
	cmpl	%esi, %r15d
	jl	.L42
.L43:
	movl	40(%rsp), %esi
	cmpl	%esi, 20(%rsp)
	jge	.L34
	movslq	20(%rsp), %r11
	movl	%esi, %eax
	movl	%r11d, %r15d
.L33:
	movl	(%r9,%r11,4), %esi
	movl	%r15d, %ecx
.L26:
	cmpl	%eax, %ecx
	jg	.L138
	movslq	%ecx, %rdx
	salq	$2, %rdx
	leaq	(%r9,%rdx), %rbx
	movl	(%rbx), %r10d
	cmpl	%r10d, %esi
	jle	.L31
	leaq	4(%r9,%rdx), %rdx
.L27:
	movq	%rdx, %rbx
	leaq	4(%rdx), %rdx
	movl	-4(%rdx), %r10d
	addl	$1, %ecx
	cmpl	%r10d, %esi
	jg	.L27
	jmp	.L164
.L28:
	cmpl	%eax, %ecx
	jg	.L138
.L91:
	movl	%r8d, (%rbx)
	addl	$1, %ecx
	movl	%r10d, (%rdi)
	subl	$1, %eax
	jmp	.L26
.L31:
	movslq	%eax, %rdx
	salq	$2, %rdx
	leaq	(%r9,%rdx), %rdi
	movl	(%rdi), %r8d
	cmpl	%r8d, %esi
	jl	.L100
	jmp	.L91
	.p2align 4,,10
	.p2align 3
.L165:
	movslq	%eax, %r8
	salq	$2, %r8
	leaq	(%r9,%r8), %rcx
	movl	(%rcx), %edi
	cmpl	%edi, %esi
	jge	.L160
.L101:
	leaq	-4(%r9,%r8), %r8
.L38:
	movq	%r8, %rcx
	leaq	-4(%r8), %r8
	movl	4(%r8), %edi
	subl	$1, %eax
	cmpl	%edi, %esi
	jl	.L38
.L160:
	cmpl	%eax, %edx
	jle	.L92
.L141:
	movl	%eax, %esi
	movl	%edx, 24(%rsp)
	movl	%eax, 16(%rsp)
	cmpl	%esi, %r15d
	jl	.L142
.L52:
	movl	12(%rsp), %esi
	cmpl	%esi, 24(%rsp)
	jge	.L43
	movslq	24(%rsp), %r11
	movl	%r11d, %r15d
.L42:
	movl	(%r9,%r11,4), %esi
	movl	12(%rsp), %eax
	movl	%r15d, %edx
.L35:
	cmpl	%eax, %edx
	jg	.L141
	movslq	%edx, %rcx
	salq	$2, %rcx
	leaq	(%r9,%rcx), %r10
	movl	(%r10), %ebx
	cmpl	%ebx, %esi
	jle	.L40
	leaq	4(%r9,%rcx), %rcx
.L36:
	movq	%rcx, %r10
	leaq	4(%rcx), %rcx
	movl	-4(%rcx), %ebx
	addl	$1, %edx
	cmpl	%ebx, %esi
	jg	.L36
	jmp	.L165
.L40:
	movslq	%eax, %r8
	salq	$2, %r8
	leaq	(%r9,%r8), %rcx
	movl	(%rcx), %edi
	cmpl	%edi, %esi
	jl	.L101
.L92:
	movl	%edi, (%r10)
	addl	$1, %edx
	movl	%ebx, (%rcx)
	subl	$1, %eax
	jmp	.L35
.L142:
	movq	%r9, %r13
	movl	%esi, %eax
.L51:
	movl	0(%r13,%r11,4), %esi
	movl	%r15d, %ecx
	movl	%eax, %edx
.L44:
	cmpl	%edx, %ecx
	jg	.L48
	movslq	%ecx, %rax
	salq	$2, %rax
	leaq	0(%r13,%rax), %r10
	movl	(%r10), %r9d
	cmpl	%r9d, %esi
	jle	.L49
	leaq	4(%r13,%rax), %rax
.L45:
	movq	%rax, %r10
	leaq	4(%rax), %rax
	movl	-4(%rax), %r9d
	addl	$1, %ecx
	cmpl	%r9d, %esi
	jg	.L45
	movslq	%edx, %rax
	salq	$2, %rax
	leaq	0(%r13,%rax), %rdi
	movl	(%rdi), %r8d
	cmpl	%r8d, %esi
	jge	.L159
.L102:
	leaq	-4(%r13,%rax), %rax
.L47:
	movq	%rax, %rdi
	leaq	-4(%rax), %rax
	movl	4(%rax), %r8d
	subl	$1, %edx
	cmpl	%r8d, %esi
	jl	.L47
.L159:
	cmpl	%edx, %ecx
	jle	.L93
.L48:
	cmpl	%edx, %r15d
	movl	%ecx, 44(%rsp)
	movl	%edx, 48(%rsp)
	jl	.L60
.L61:
	movl	16(%rsp), %esi
	cmpl	%esi, 44(%rsp)
	jge	.L166
	movslq	44(%rsp), %r11
	movl	%esi, %eax
	movl	%r11d, %r15d
	jmp	.L51
	.p2align 4,,10
	.p2align 3
.L167:
	movslq	%r8d, %rax
	salq	$2, %rax
	leaq	0(%r13,%rax), %rdx
	movl	(%rdx), %ecx
	cmpl	%ecx, %esi
	jge	.L55
.L103:
	leaq	-4(%r13,%rax), %rax
	.p2align 4,,10
	.p2align 3
.L56:
	movq	%rax, %rdx
	leaq	-4(%rax), %rax
	movl	4(%rax), %ecx
	subl	$1, %r8d
	cmpl	%ecx, %esi
	jl	.L56
	cmpl	%r8d, %r9d
	jle	.L94
.L57:
	cmpl	%r8d, %r15d
	jl	.L146
.L70:
	cmpl	%r9d, 48(%rsp)
	jle	.L61
	movslq	%r9d, %r11
	movl	%r11d, %r15d
.L60:
	movl	0(%r13,%r11,4), %esi
	movl	48(%rsp), %r8d
	movl	%r15d, %r9d
.L53:
	cmpl	%r8d, %r9d
	jg	.L57
	movslq	%r9d, %rax
	salq	$2, %rax
	leaq	0(%r13,%rax), %r10
	movl	(%r10), %edi
	cmpl	%edi, %esi
	jle	.L58
	leaq	4(%r13,%rax), %rax
	.p2align 4,,10
	.p2align 3
.L54:
	movq	%rax, %r10
	leaq	4(%rax), %rax
	movl	-4(%rax), %edi
	addl	$1, %r9d
	cmpl	%edi, %esi
	jg	.L54
	jmp	.L167
.L55:
	cmpl	%r8d, %r9d
	jg	.L57
.L94:
	movl	%ecx, (%r10)
	addl	$1, %r9d
	movl	%edi, (%rdx)
	subl	$1, %r8d
	jmp	.L53
.L166:
	movq	%r13, %r9
	jmp	.L52
.L58:
	movslq	%r8d, %rax
	salq	$2, %rax
	leaq	0(%r13,%rax), %rdx
	movl	(%rdx), %ecx
	cmpl	%ecx, %esi
	jl	.L103
	jmp	.L94
.L146:
	movl	%r9d, 56(%rsp)
	movl	%r15d, %esi
.L69:
	movl	0(%r13,%r11,4), %edi
	movl	%r8d, %r14d
	movl	%esi, %r15d
.L62:
	cmpl	%r14d, %r15d
	jg	.L66
	movslq	%r15d, %rax
	salq	$2, %rax
	leaq	0(%r13,%rax), %r9
	movl	(%r9), %r10d
	cmpl	%edi, %r10d
	jge	.L67
	leaq	4(%r13,%rax), %rax
	.p2align 4,,10
	.p2align 3
.L63:
	movq	%rax, %r9
	leaq	4(%rax), %rax
	movl	-4(%rax), %r10d
	addl	$1, %r15d
	cmpl	%r10d, %edi
	jg	.L63
	movslq	%r14d, %rax
	salq	$2, %rax
	leaq	0(%r13,%rax), %rdx
	movl	(%rdx), %ecx
	cmpl	%ecx, %edi
	jge	.L64
.L104:
	leaq	-4(%r13,%rax), %rax
	.p2align 4,,10
	.p2align 3
.L65:
	movq	%rax, %rdx
	leaq	-4(%rax), %rax
	movl	4(%rax), %ecx
	subl	$1, %r14d
	cmpl	%ecx, %edi
	jl	.L65
	cmpl	%r14d, %r15d
	jle	.L95
.L66:
	cmpl	%r14d, %esi
	jl	.L78
.L79:
	cmpl	%r8d, %r15d
	jge	.L168
	movslq	%r15d, %r11
	movq	%r11, %rsi
	jmp	.L69
	.p2align 4,,10
	.p2align 3
.L169:
	movslq	%ebp, %rax
	salq	$2, %rax
	leaq	0(%r13,%rax), %rdx
	movl	(%rdx), %ecx
	cmpl	%edi, %ecx
	jle	.L73
.L105:
	leaq	-4(%r13,%rax), %rax
	.p2align 4,,10
	.p2align 3
.L74:
	movq	%rax, %rdx
	leaq	-4(%rax), %rax
	movl	4(%rax), %ecx
	subl	$1, %ebp
	cmpl	%ecx, %edi
	jl	.L74
	cmpl	%ebp, %r12d
	jle	.L96
.L75:
	cmpl	%ebp, %esi
	jl	.L87
.L88:
	cmpl	%r14d, %r12d
	jge	.L79
	movslq	%r12d, %r11
	movq	%r11, %rsi
.L78:
	movl	0(%r13,%r11,4), %edi
	movl	%r14d, %ebp
	movl	%esi, %r12d
.L71:
	cmpl	%ebp, %r12d
	jg	.L75
	movslq	%r12d, %rax
	salq	$2, %rax
	leaq	0(%r13,%rax), %r9
	movl	(%r9), %r10d
	cmpl	%r10d, %edi
	jle	.L76
	leaq	4(%r13,%rax), %rax
	.p2align 4,,10
	.p2align 3
.L72:
	movq	%rax, %r9
	leaq	4(%rax), %rax
	movl	-4(%rax), %r10d
	addl	$1, %r12d
	cmpl	%r10d, %edi
	jg	.L72
	jmp	.L169
	.p2align 4,,10
	.p2align 3
.L171:
	movslq	%edx, %rax
	salq	$2, %rax
	leaq	0(%r13,%rax), %rcx
	movl	(%rcx), %r11d
	cmpl	%r11d, %edi
	jge	.L82
.L106:
	leaq	-4(%r13,%rax), %rax
	.p2align 4,,10
	.p2align 3
.L83:
	movq	%rax, %rcx
	leaq	-4(%rax), %rax
	movl	4(%rax), %r11d
	subl	$1, %edx
	cmpl	%r11d, %edi
	jl	.L83
	cmpl	%edx, %ebx
	jle	.L97
.L84:
	cmpl	%edx, %esi
	jl	.L170
.L86:
	cmpl	%ebx, %ebp
	jle	.L88
	movslq	%ebx, %r11
	movq	%r11, %rsi
.L87:
	movl	0(%r13,%r11,4), %edi
	movl	%ebp, %edx
	movl	%esi, %ebx
.L80:
	cmpl	%edx, %ebx
	jg	.L84
	movslq	%ebx, %rax
	salq	$2, %rax
	leaq	0(%r13,%rax), %r9
	movl	(%r9), %r10d
	cmpl	%r10d, %edi
	jle	.L85
	leaq	4(%r13,%rax), %rax
	.p2align 4,,10
	.p2align 3
.L81:
	movq	%rax, %r9
	leaq	4(%rax), %rax
	movl	-4(%rax), %r10d
	addl	$1, %ebx
	cmpl	%r10d, %edi
	jg	.L81
	jmp	.L171
.L82:
	cmpl	%edx, %ebx
	jg	.L84
.L97:
	movl	%r11d, (%r9)
	addl	$1, %ebx
	movl	%r10d, (%rcx)
	subl	$1, %edx
	jmp	.L80
.L73:
	cmpl	%ebp, %r12d
	jg	.L75
.L96:
	movl	%ecx, (%r9)
	addl	$1, %r12d
	movl	%r10d, (%rdx)
	subl	$1, %ebp
	jmp	.L71
.L170:
	movq	%r13, %rdi
	movl	%r8d, 60(%rsp)
	call	quicksort
	movl	60(%rsp), %r8d
	jmp	.L86
.L64:
	cmpl	%r14d, %r15d
	jg	.L66
.L95:
	movl	%ecx, (%r9)
	addl	$1, %r15d
	movl	%r10d, (%rdx)
	subl	$1, %r14d
	jmp	.L62
.L85:
	movslq	%edx, %rax
	salq	$2, %rax
	leaq	0(%r13,%rax), %rcx
	movl	(%rcx), %r11d
	cmpl	%r11d, %edi
	jl	.L106
	jmp	.L97
.L76:
	movslq	%ebp, %rax
	salq	$2, %rax
	leaq	0(%r13,%rax), %rdx
	movl	(%rdx), %ecx
	cmpl	%ecx, %edi
	jl	.L105
	jmp	.L96
	.p2align 4,,10
	.p2align 3
.L67:
	movslq	%r14d, %rax
	salq	$2, %rax
	leaq	0(%r13,%rax), %rdx
	movl	(%rdx), %ecx
	cmpl	%ecx, %edi
	jl	.L104
	jmp	.L95
.L168:
	movl	56(%rsp), %r9d
	jmp	.L70
.L49:
	movslq	%edx, %rax
	salq	$2, %rax
	leaq	0(%r13,%rax), %rdi
	movl	(%rdi), %r8d
	cmpl	%r8d, %esi
	jl	.L102
.L93:
	movl	%r8d, (%r10)
	addl	$1, %ecx
	movl	%r9d, (%rdi)
	subl	$1, %edx
	jmp	.L44
.L19:
	cmpl	%eax, %ecx
	jg	.L21
	jmp	.L90
	.cfi_endproc
.LFE40:
	.size	quicksort, .-quicksort
	.section	.text.unlikely
.LCOLDE5:
	.text
.LHOTE5:
	.section	.text.unlikely
.LCOLDB6:
	.text
.LHOTB6:
	.p2align 4,,15
	.globl	benchmark_quicksort
	.type	benchmark_quicksort, @function
benchmark_quicksort:
.LFB41:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	pushq	%rbx
	.cfi_def_cfa_offset 24
	.cfi_offset 3, -24
	movq	%rdi, %rbp
	xorl	%esi, %esi
	subq	$8, %rsp
	.cfi_def_cfa_offset 32
.L180:
	movslq	%esi, %rax
	movl	%esi, %ebx
	movl	$99, %edx
	movl	0(%rbp,%rax,4), %r8d
.L173:
	movslq	%ebx, %rax
	salq	$2, %rax
	leaq	0(%rbp,%rax), %r9
	movl	(%r9), %r10d
	cmpl	%r10d, %r8d
	jle	.L178
	leaq	4(%rbp,%rax), %rax
	.p2align 4,,10
	.p2align 3
.L174:
	movq	%rax, %r9
	leaq	4(%rax), %rax
	movl	-4(%rax), %r10d
	addl	$1, %ebx
	cmpl	%r10d, %r8d
	jg	.L174
	movslq	%edx, %rax
	salq	$2, %rax
	leaq	0(%rbp,%rax), %rdi
	movl	(%rdi), %ecx
	cmpl	%ecx, %r8d
	jge	.L175
.L182:
	leaq	-4(%rbp,%rax), %rax
	.p2align 4,,10
	.p2align 3
.L176:
	movq	%rax, %rdi
	leaq	-4(%rax), %rax
	movl	4(%rax), %ecx
	subl	$1, %edx
	cmpl	%ecx, %r8d
	jl	.L176
	cmpl	%ebx, %edx
	jge	.L181
.L177:
	cmpl	%edx, %esi
	jl	.L189
	cmpl	$98, %ebx
	jg	.L190
.L183:
	movl	%ebx, %esi
	jmp	.L180
.L175:
	cmpl	%edx, %ebx
	jg	.L177
.L181:
	addl	$1, %ebx
	subl	$1, %edx
	movl	%ecx, (%r9)
	cmpl	%edx, %ebx
	movl	%r10d, (%rdi)
	jle	.L173
	jmp	.L177
.L189:
	movq	%rbp, %rdi
	call	quicksort
	cmpl	$98, %ebx
	jle	.L183
.L190:
	addq	$8, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 24
	popq	%rbx
	.cfi_def_cfa_offset 16
	popq	%rbp
	.cfi_def_cfa_offset 8
	ret
.L178:
	.cfi_restore_state
	movslq	%edx, %rax
	salq	$2, %rax
	leaq	0(%rbp,%rax), %rdi
	movl	(%rdi), %ecx
	cmpl	%ecx, %r8d
	jl	.L182
	jmp	.L181
	.cfi_endproc
.LFE41:
	.size	benchmark_quicksort, .-benchmark_quicksort
	.section	.text.unlikely
.LCOLDE6:
	.text
.LHOTE6:
	.section	.text.unlikely
.LCOLDB9:
	.text
.LHOTB9:
	.p2align 4,,15
	.globl	fill_array
	.type	fill_array, @function
fill_array:
.LFB42:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	pushq	%rbx
	.cfi_def_cfa_offset 24
	.cfi_offset 3, -24
	subq	$24, %rsp
	.cfi_def_cfa_offset 48
	testl	%esi, %esi
	jne	.L192
	leaq	400(%rdi), %rbp
	movq	%rdi, %rbx
	.p2align 4,,10
	.p2align 3
.L193:
	call	rand
	addq	$4, %rbx
	movl	%eax, -4(%rbx)
	cmpq	%rbp, %rbx
	jne	.L193
.L200:
	addq	$24, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 24
	xorl	%eax, %eax
	popq	%rbx
	.cfi_def_cfa_offset 16
	popq	%rbp
	.cfi_def_cfa_offset 8
	ret
	.p2align 4,,10
	.p2align 3
.L192:
	.cfi_restore_state
	movq	%rdi, %rax
	andl	$15, %eax
	shrq	$2, %rax
	negq	%rax
	andl	$3, %eax
	je	.L201
	cmpl	$1, %eax
	movl	$0, (%rdi)
	je	.L202
	cmpl	$3, %eax
	movl	$1, 4(%rdi)
	jne	.L203
	movl	$2, 8(%rdi)
	movl	$97, %r8d
	movl	$3, %esi
.L195:
	movl	$100, %r9d
	movl	%eax, %edx
	movl	$96, %r10d
	subl	%eax, %r9d
	movl	$24, %ecx
.L194:
	movl	%esi, 12(%rsp)
	leaq	(%rdi,%rdx,4), %rdx
	xorl	%eax, %eax
	movd	12(%rsp), %xmm2
	movdqa	.LC8(%rip), %xmm1
	pshufd	$0, %xmm2, %xmm0
	paddd	.LC7(%rip), %xmm0
	.p2align 4,,10
	.p2align 3
.L196:
	addl	$1, %eax
	addq	$16, %rdx
	movaps	%xmm0, -16(%rdx)
	paddd	%xmm1, %xmm0
	cmpl	%ecx, %eax
	jb	.L196
	movl	%r8d, %edx
	leal	(%r10,%rsi), %eax
	subl	%r10d, %edx
	cmpl	%r10d, %r9d
	je	.L200
	movslq	%eax, %rcx
	cmpl	$1, %edx
	movl	%eax, (%rdi,%rcx,4)
	leal	1(%rax), %ecx
	je	.L200
	movslq	%ecx, %rsi
	addl	$2, %eax
	cmpl	$2, %edx
	movl	%ecx, (%rdi,%rsi,4)
	je	.L200
	movslq	%eax, %rdx
	movl	%eax, (%rdi,%rdx,4)
	addq	$24, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 24
	xorl	%eax, %eax
	popq	%rbx
	.cfi_def_cfa_offset 16
	popq	%rbp
	.cfi_def_cfa_offset 8
	ret
.L201:
	.cfi_restore_state
	movl	$100, %r10d
	movl	$25, %ecx
	movl	$100, %r9d
	xorl	%edx, %edx
	movl	$100, %r8d
	xorl	%esi, %esi
	jmp	.L194
.L203:
	movl	$98, %r8d
	movl	$2, %esi
	jmp	.L195
.L202:
	movl	$99, %r8d
	movl	$1, %esi
	jmp	.L195
	.cfi_endproc
.LFE42:
	.size	fill_array, .-fill_array
	.section	.text.unlikely
.LCOLDE9:
	.text
.LHOTE9:
	.section	.text.unlikely
.LCOLDB10:
	.section	.text.startup,"ax",@progbits
.LHOTB10:
	.p2align 4,,15
	.globl	main
	.type	main, @function
main:
.LFB43:
	.cfi_startproc
	pushq	%r12
	.cfi_def_cfa_offset 16
	.cfi_offset 12, -16
	pushq	%rbp
	.cfi_def_cfa_offset 24
	.cfi_offset 6, -24
	movl	$400, %edi
	pushq	%rbx
	.cfi_def_cfa_offset 32
	.cfi_offset 3, -32
	xorl	%ebx, %ebx
	call	malloc
	movslq	%eax, %r12
	movq	%r12, %rbp
	.p2align 4,,10
	.p2align 3
.L214:
	call	rand
	addq	$4, %rbx
	movl	%eax, -4(%rbx,%rbp)
	cmpq	$400, %rbx
	jne	.L214
	movq	%r12, %rdi
	movl	$99, %edx
	xorl	%esi, %esi
	call	quicksort
	movq	%r12, %rdi
	call	free
	popq	%rbx
	.cfi_def_cfa_offset 24
	xorl	%eax, %eax
	popq	%rbp
	.cfi_def_cfa_offset 16
	popq	%r12
	.cfi_def_cfa_offset 8
	ret
	.cfi_endproc
.LFE43:
	.size	main, .-main
	.section	.text.unlikely
.LCOLDE10:
	.section	.text.startup
.LHOTE10:
	.section	.rodata.cst16,"aM",@progbits,16
	.align 16
.LC7:
	.long	0
	.long	1
	.long	2
	.long	3
	.align 16
.LC8:
	.long	4
	.long	4
	.long	4
	.long	4
	.ident	"GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.10) 5.4.0 20160609"
	.section	.note.GNU-stack,"",@progbits
